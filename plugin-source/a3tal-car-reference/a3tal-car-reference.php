<?php
/**
 * Plugin Name: A3tal Car Reference Engine
 * Description: Verified technical data pages for makes, models and service specifications.
 * Version: 1.0.0
 * Requires PHP: 7.4
 * Author: A3tal.com
 * Update URI: https://github.com/marwanile1-cyber/a3tal
 */
defined('ABSPATH') || exit;
final class A3tal_Car_Reference_Engine {
    const TYPE='a3_car_ref';
    const META='_a3cr_verified_data';
    const NS='a3tal-car-reference/v1';
    public static function boot() {
        add_action('init',[__CLASS__,'register'],9);
        add_action('rest_api_init',[__CLASS__,'routes']);
        add_filter('template_include',[__CLASS__,'template'],30);
        add_action('wp_enqueue_scripts',[__CLASS__,'css']);
        add_filter('wpseo_robots',[__CLASS__,'yoast_robots']);
        add_filter('wp_robots',[__CLASS__,'robots']);
        add_filter('wpseo_title',[__CLASS__,'seo_title']);
        add_filter('wpseo_metadesc',[__CLASS__,'seo_description']);
        add_action('wp_head',[__CLASS__,'schema'],20);
        add_action('add_meta_boxes',[__CLASS__,'meta_boxes']);
        add_action('save_post_'.self::TYPE,[__CLASS__,'save_meta'],10,2);
    }
    public static function register() {
        register_post_type(self::TYPE,[
            'label'=>'دليل المواصفات الفنية',
            'labels'=>['name'=>'دليل المواصفات الفنية','singular_name'=>'صفحة مواصفات','add_new_item'=>'إضافة صفحة فنية'],
            'public'=>true,'hierarchical'=>true,'has_archive'=>'car-reference',
            'rewrite'=>['slug'=>'car-reference','with_front'=>false,'hierarchical'=>true],
            'show_in_rest'=>true,'rest_base'=>'car-reference-records',
            'menu_icon'=>'dashicons-car','supports'=>['title','editor','excerpt','thumbnail','revisions','page-attributes'],
        ]);
    }
    public static function activate(){ self::register(); flush_rewrite_rules(false); }
    public static function deactivate(){flush_rewrite_rules(false);}
    public static function data($id) {
        $value=json_decode((string)get_post_meta($id,self::META,true),true);
        return is_array($value)?$value:[];
    }
    private static function clean($data) {
        $kind=sanitize_key((string)($data['kind']??''));
        $out=[
          'kind'=>in_array($kind,['brand','model','spec'],true)?$kind:'',
          'market'=>sanitize_text_field((string)($data['market']??'')),
          'years'=>sanitize_text_field((string)($data['years']??'')),
          'engine'=>sanitize_text_field((string)($data['engine']??'')),
          'category'=>sanitize_key((string)($data['category']??'')),
          'reviewed_at'=>sanitize_text_field((string)($data['reviewed_at']??'')),
          'facts'=>[],'sources'=>[],
        ];
        foreach(array_slice((array)($data['facts']??[]),0,50) as $row) {
          if(!is_array($row))continue;
          $label=sanitize_text_field((string)($row['label']??''));
          $value=sanitize_text_field((string)($row['value']??''));
          if($label!=='' && $value!=='')$out['facts'][]=['label'=>$label,'value'=>$value];
        }
        foreach(array_slice((array)($data['sources']??[]),0,15) as $row) {
          if(!is_array($row))continue;
          $url=esc_url_raw((string)($row['url']??''),['https']);
          if($url && wp_http_validate_url($url))$out['sources'][]=[
            'title'=>sanitize_text_field((string)($row['title']??'المصدر')),
            'url'=>$url,
          ];
        }
        return $out;
    }
    public static function meta_boxes(){
        add_meta_box('a3cr-data','بيانات فنية ومصادر موثقة (JSON)',[__CLASS__,'meta_box'],self::TYPE,'normal','high');
    }
    public static function meta_box($post){
        wp_nonce_field('a3cr_meta_save','a3cr_nonce');
        $json=get_post_meta($post->ID,self::META,true);
        echo '<p>kind: brand / model / spec. يجب إدخال المراجع الحقيقية والصورة البارزة قبل النشر.</p>';
        echo '<textarea rows="12" spellcheck="false" style="width:100%;direction:ltr;font-family:monospace" name="a3cr_json">'.esc_textarea($json?:'{"kind":"model","market":"مصر","years":"","engine":"","facts":[],"sources":[]}').'</textarea>';
    }
    public static function save_meta($post_id,$post){
        if(!isset($_POST['a3cr_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['a3cr_nonce'])),'a3cr_meta_save'))return;
        if(defined('DOING_AUTOSAVE') && DOING_AUTOSAVE)return;
        if(!current_user_can('edit_post',$post_id))return;
        $raw=isset($_POST['a3cr_json']) && is_string($_POST['a3cr_json'])?wp_unslash($_POST['a3cr_json']):'';
        $data=json_decode($raw,true);
        if(is_array($data))update_post_meta($post_id,self::META,wp_json_encode(self::clean($data),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
    }
    public static function routes() {
        register_rest_route(self::NS,'/health',[
          'methods'=>'GET','permission_callback'=>'__return_true',
          'callback'=>function(){
            $count=wp_count_posts(self::TYPE);
            return ['ok'=>true,'name'=>'A3tal Car Reference Engine','version'=>'1.0.0',
             'published'=>(int)($count->publish??0),'drafts'=>(int)($count->draft??0),
             'archive'=>get_post_type_archive_link(self::TYPE)];
          }
        ]);
        register_rest_route(self::NS,'/upsert',[
          'methods'=>'POST','permission_callback'=>[__CLASS__,'auth'],
          'callback'=>[__CLASS__,'upsert'],
        ]);
    }
    public static function auth($request) {
        if(current_user_can('manage_options'))return true;
        $stored=(string)get_option('a3tal_direct_bridge_api_key','');
        $given=(string)$request->get_header('x-a3tal-key');
        if($stored!=='' && $given!=='' && hash_equals($stored,$given))return true;
        return new WP_Error('a3cr_auth','Admin bridge key required',['status'=>403]);
    }
    public static function upsert($request) {
        $json=$request->get_json_params();
        $items=isset($json['items']) && is_array($json['items'])?$json['items']:[];
        if(!$items || count($items)>25)return new WP_Error('a3cr_limit','Send 1-25 items',['status'=>400]);
        $results=[];
        foreach($items as $item){
            $out=self::upsert_one($item);
            $results[]=is_wp_error($out)?['ok'=>false,'error'=>$out->get_error_message()]:['ok'=>true]+$out;
        }
        return rest_ensure_response(['ok'=>!in_array(false,array_column($results,'ok'),true),'results'=>$results]);
    }
    private static function upsert_one($item) {
        if(!is_array($item))return new WP_Error('a3cr_item','Invalid item');
        $title=sanitize_text_field((string)($item['title']??''));
        $slug=(string)($item['slug']??'');
        $kind=sanitize_key((string)($item['kind']??''));
        if(!$title || !preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/D',$slug) ||
           !in_array($kind,['brand','model','spec'],true))return new WP_Error('a3cr_identity','Invalid title, slug, or kind');
        $parent_path=trim((string)($item['parent_path']??''),'/');
        $depth=$parent_path===''?0:count(explode('/',$parent_path));
        if(($kind==='brand'&&$depth!==0)||($kind==='model'&&$depth!==1)||($kind==='spec'&&$depth!==2))return new WP_Error('a3cr_parent_depth','Invalid parent depth');
        $parent_id=0;
        if($depth){
            if(!preg_match('#^[a-z0-9-]+(?:/[a-z0-9-]+)*$#D',$parent_path))return new WP_Error('a3cr_parent_path','Invalid parent path');
            $parent=get_page_by_path($parent_path,OBJECT,self::TYPE);
            if(!$parent)return new WP_Error('a3cr_parent_missing','Parent must exist');
            $parent_kind=self::data($parent->ID)['kind']??'';
            if(($kind==='model'&&$parent_kind!=='brand')||($kind==='spec'&&$parent_kind!=='model'))return new WP_Error('a3cr_parent_kind','Wrong parent kind');
            $parent_id=(int)$parent->ID;
        }
        $path=($parent_path?$parent_path.'/':'').$slug;
        $existing=get_page_by_path($path,OBJECT,self::TYPE);
        if($existing && $existing->post_status==='publish' && empty($item['allow_update_published']))return new WP_Error('a3cr_live_protected','Explicit allow_update_published required');
        $data=self::clean((array)($item['data']??[]));
        $data['kind']=$kind;
        $content=wp_kses_post((string)($item['content']??''));
        $status=(string)($item['status']??'draft');
        if(!in_array($status,['draft','pending','publish'],true))return new WP_Error('a3cr_status','Invalid status');
        $image_id=absint($item['featured_image_id']??($existing?get_post_thumbnail_id($existing->ID):0));
        if($status==='publish' && (!$content || !$data['sources'] ||
          !$image_id || !wp_attachment_is_image($image_id) ||
          ($kind==='spec' && count($data['facts'])<2)))return new WP_Error('a3cr_quality','Publishing requires content, sources, photo and factual rows for specs');
        $post=['post_type'=>self::TYPE,'post_status'=>$status,
          'post_title'=>$title,'post_name'=>$slug,'post_parent'=>$parent_id,
          'post_content'=>$content,'post_excerpt'=>sanitize_text_field((string)($item['excerpt']??''))];
        if($existing)$post['ID']=(int)$existing->ID;
        $id=wp_insert_post(wp_slash($post),true);
        if(is_wp_error($id))return $id;
        update_post_meta($id,self::META,wp_json_encode($data,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
        if($image_id)set_post_thumbnail($id,$image_id);
        if(!empty($item['meta_title']))update_post_meta($id,'_yoast_wpseo_title',sanitize_text_field((string)$item['meta_title']));
        if(!empty($item['meta_description']))update_post_meta($id,'_yoast_wpseo_metadesc',sanitize_text_field((string)$item['meta_description']));
        return ['id'=>(int)$id,'status'=>$status,'url'=>get_permalink($id)];
    }
    public static function template($template) {
        if(is_post_type_archive(self::TYPE)||is_singular(self::TYPE))
          return plugin_dir_path(__FILE__).(is_post_type_archive(self::TYPE)?'archive.php':'single.php');
        return $template;
    }
    public static function css(){
        if(is_post_type_archive(self::TYPE)||is_singular(self::TYPE))
            wp_enqueue_style('a3cr-style',plugins_url('reference.css',__FILE__),[],'1.0.0');
    }
    private static function has_published(){
        return (bool)get_posts(['post_type'=>self::TYPE,'post_status'=>'publish','fields'=>'ids','numberposts'=>1]);
    }
    public static function yoast_robots($robots){
        return is_post_type_archive(self::TYPE)&&!self::has_published()?'noindex,follow':$robots;
    }
    public static function robots($robots){
        if(is_post_type_archive(self::TYPE)&&!self::has_published())$robots['noindex']=true;
        return $robots;
    }
    public static function seo_title($title){
        return is_post_type_archive(self::TYPE)?'دليل المواصفات الفنية للسيارات | أعطال.كوم':$title;
    }
    public static function seo_description($description){
        return is_post_type_archive(self::TYPE)?'مواصفات الصيانة والزيوت والإطارات والبطاريات حسب الماركة والموديل والمحرك من مصادر موثقة.':$description;
    }
    public static function schema(){
        if(!is_singular(self::TYPE))return;
        $post=get_queried_object();
        $data=self::data($post->ID);
        if(($data['kind']??'')!=='spec'||empty($data['sources']))return;
        $schema=['@context'=>'https://schema.org','@type'=>'TechArticle',
          'headline'=>get_the_title($post),'url'=>get_permalink($post),
          'inLanguage'=>'ar','citation'=>array_column($data['sources'],'url'),
          'dateModified'=>get_post_modified_time('c',true,$post)];
        if(has_post_thumbnail($post))$schema['image']=get_the_post_thumbnail_url($post,'full');
        echo '<script type="application/ld+json">'.wp_json_encode($schema,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_HEX_TAG).'</script>';
    }
    public static function card($post){
        $data=self::data($post->ID);
        echo '<a class="a3cr-card" href="'.esc_url(get_permalink($post)).'">';
        if(has_post_thumbnail($post))echo get_the_post_thumbnail($post,'medium',['loading'=>'lazy']);
        echo '<strong>'.esc_html(get_the_title($post)).'</strong>';
        if(!empty($data['years']))echo '<small>'.esc_html($data['years']).'</small>';
        echo '<span>عرض التفاصيل ←</span></a>';
    }
}
A3tal_Car_Reference_Engine::boot();
register_activation_hook(__FILE__,['A3tal_Car_Reference_Engine','activate']);
register_deactivation_hook(__FILE__,['A3tal_Car_Reference_Engine','deactivate']);

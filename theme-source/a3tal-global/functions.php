<?php
if (!defined('ABSPATH')) exit;
define('A3G_VERSION','1.7.2');

function a3g_setup(){
  add_theme_support('title-tag');
  add_theme_support('post-thumbnails');
  add_theme_support('custom-logo',['height'=>100,'width'=>320,'flex-height'=>true,'flex-width'=>true]);
  add_theme_support('responsive-embeds');
  add_theme_support('html5',['search-form','gallery','caption','style','script']);
  register_nav_menus(['primary'=>'القائمة الرئيسية','footer'=>'قائمة الفوتر']);
}
add_action('after_setup_theme','a3g_setup');

function a3g_assets(){
  wp_enqueue_style('a3g-fonts','https://fonts.googleapis.com/css2?family=Alexandria:wght@500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap',[],null);
  wp_enqueue_style('a3g-style',get_stylesheet_uri(),['a3g-fonts'],A3G_VERSION);
  wp_enqueue_script('a3g-theme',get_template_directory_uri().'/assets/js/theme.js',[],A3G_VERSION,true);
}
add_action('wp_enqueue_scripts','a3g_assets');
add_action('wp_head',function(){echo '<meta name="theme-color" content="#091522">'.PHP_EOL;},1);

function a3g_cat_link($id){$u=get_category_link((int)$id);return is_wp_error($u)?home_url('/'):$u;}
function a3g_search($q=''){return add_query_arg('s',$q,home_url('/'));}
function a3g_query($args=[]){return new WP_Query(wp_parse_args($args,['post_type'=>'post','post_status'=>'publish','ignore_sticky_posts'=>true]));}
function a3g_primary_cat($id=0){$id=$id?:get_the_ID();$c=get_the_category($id);return $c?($c[0]??null):null;}
function a3g_excerpt($id=0,$words=22){$id=$id?:get_the_ID();$x=get_the_excerpt($id);if(!$x)$x=wp_strip_all_tags((string)get_post_field('post_content',$id));return wp_trim_words($x,$words);}
function a3g_read_time($id=0){$id=$id?:get_the_ID();$t=wp_strip_all_tags((string)get_post_field('post_content',$id));$w=preg_split('/\s+/u',trim($t));return max(1,(int)ceil(count(array_filter((array)$w))/220));}
function a3g_is_diagnostic($id=0){$id=$id?:get_the_ID();return has_category([2,8,9,10,11,12,13,14,15,18,298],$id);}

function a3g_logo(){
  if(has_custom_logo()){ echo get_custom_logo(); return; }
  echo '<span class="g-logo-mark" aria-hidden="true"><span></span></span><span class="g-logo-copy"><strong>أعطال</strong><small>A3tal.com</small></span>';
}

function a3g_icon($name){
  $icons=[
    'search'=>'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-3.7-3.7"></path></svg>',
    'car'=>'<svg viewBox="0 0 24 24"><path d="M5 17h14l-1.4-6H6.4L5 17Z"></path><path d="m7 11 1.5-4h7L17 11"></path><circle cx="7.5" cy="18.5" r="1.5"></circle><circle cx="16.5" cy="18.5" r="1.5"></circle></svg>',
    'wrench'=>'<svg viewBox="0 0 24 24"><path d="M14.7 6.3a5 5 0 0 0-6.8 6.8L3 18l3 3 4.9-4.9a5 5 0 0 0 6.8-6.8l-3 3-3-3 3-3Z"></path></svg>',
    'compare'=>'<svg viewBox="0 0 24 24"><path d="M7 7h11"></path><path d="m15 4 3 3-3 3"></path><path d="M17 17H6"></path><path d="m9 14-3 3 3 3"></path></svg>',
    'pin'=>'<svg viewBox="0 0 24 24"><path d="M12 21s6-5.2 6-11a6 6 0 1 0-12 0c0 5.8 6 11 6 11Z"></path><circle cx="12" cy="10" r="2"></circle></svg>',
    'bolt'=>'<svg viewBox="0 0 24 24"><path d="m13 2-8 12h6l-1 8 9-13h-6l0-7Z"></path></svg>',
    'gear'=>'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"></circle><path d="M19 13.5v-3l-2-.6a6 6 0 0 0-.7-1.7l1-1.8-2.1-2.1-1.8 1A6 6 0 0 0 11.5 5L11 3H8l-.6 2a6 6 0 0 0-1.7.7l-1.8-1-2.1 2.1 1 1.8A6 6 0 0 0 2 10.5l-2 .5v3l2 .6c.2.6.4 1.2.7 1.7l-1 1.8 2.1 2.1 1.8-1c.5.3 1.1.5 1.7.7L8 22h3l.6-2a6 6 0 0 0 1.7-.7l1.8 1 2.1-2.1-1-1.8c.3-.5.5-1.1.7-1.7l2.1-.7Z" transform="translate(2 -1) scale(.84)"></path></svg>',
    'leaf'=>'<svg viewBox="0 0 24 24"><path d="M20 4C11 4 5 8 5 15c0 3 2 5 5 5 7 0 10-7 10-16Z"></path><path d="M4 21c3-7 7-10 13-13"></path></svg>',
    'calendar'=>'<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"></rect><path d="M7 3v4M17 3v4M3 10h18"></path></svg>',
    'oil'=>'<svg viewBox="0 0 24 24"><path d="M12 3s6 7 6 12a6 6 0 1 1-12 0c0-5 6-12 6-12Z"></path></svg>',
    'filter'=>'<svg viewBox="0 0 24 24"><path d="M4 4h16l-6 7v7l-4 2v-9L4 4Z"></path></svg>',
    'menu'=>'<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"></path></svg>'
  ];
  return '<span class="g-icon" aria-hidden="true">'.($icons[$name]??$icons['car']).'</span>';
}

function a3g_card($id=0,$class=''){
  $id=$id?:get_the_ID();$cat=a3g_primary_cat($id);?>
  <article class="g-card <?php echo esc_attr($class); ?>">
    <a class="g-card-media" href="<?php echo esc_url(get_permalink($id)); ?>">
      <?php if(has_post_thumbnail($id)){echo get_the_post_thumbnail($id,'large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL</span>';} ?>
    </a>
    <div class="g-card-body">
      <?php if($cat): ?><a class="g-card-tag" href="<?php echo esc_url(get_category_link($cat)); ?>"><?php echo esc_html($cat->name); ?></a><?php endif; ?>
      <h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3>
      <p><?php echo esc_html(a3g_excerpt($id,15)); ?></p>
      <div class="g-meta"><span><?php echo esc_html(get_the_modified_date('j M',$id)); ?></span><span><?php echo esc_html(a3g_read_time($id)); ?> دقائق</span></div>
    </div>
  </article><?php
}

function a3g_price_card($id=0){
  $id=$id?:get_the_ID();?>
  <article class="g-price-card">
    <a class="g-price-media" href="<?php echo esc_url(get_permalink($id)); ?>"><?php if(has_post_thumbnail($id)){echo get_the_post_thumbnail($id,'large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL</span>';} ?></a>
    <div class="g-price-body"><h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3><span>السعر والمواصفات والتفاصيل</span></div>
  </article><?php
}

function a3g_compact($id=0){
  $id=$id?:get_the_ID();?>
  <article class="g-compact">
    <a class="g-compact-media" href="<?php echo esc_url(get_permalink($id)); ?>"><?php if(has_post_thumbnail($id)){echo get_the_post_thumbnail($id,'medium_large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3</span>';} ?></a>
    <div><h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3><div class="g-meta"><span><?php echo esc_html(get_the_modified_date('j M',$id)); ?></span></div></div>
  </article><?php
}

function a3g_heading_ids($content){
  if(!is_singular())return $content;$used=[];
  return preg_replace_callback('/<h([23])([^>]*)>(.*?)<\/h\1>/isu',function($m)use(&$used){
    if(preg_match('/\sid=["\'][^"\']+["\']/i',$m[2]))return $m[0];
    $plain=trim(wp_strip_all_tags($m[3]));$base=sanitize_title($plain);if(!$base)$base='section';$id=$base;$n=2;while(isset($used[$id])){$id=$base.'-'.$n++;}$used[$id]=1;
    return '<h'.$m[1].$m[2].' id="'.esc_attr($id).'">'.$m[3].'</h'.$m[1].'>';
  },$content);
}
add_filter('the_content','a3g_heading_ids',8);

function a3g_toc(){
  $content=(string)get_post_field('post_content',get_the_ID());preg_match_all('/<h2[^>]*>(.*?)<\/h2>/isu',$content,$m);$out=[];
  foreach($m[1]??[] as $raw){$t=trim(wp_strip_all_tags($raw));if($t)$out[]=['t'=>$t,'id'=>sanitize_title($t)];}
  return $out;
}



function a3g_responsive_tables($content){
  if(!is_singular()) return $content;
  $content=preg_replace('/<div class=["\']g-table-wrap["\']>\s*(<table\b.*?<\/table>)\s*<\/div>/isu','$1',$content);
  return preg_replace_callback('/<table\b[^>]*>.*?<\/table>/isu',static function($m){
    return '<div class="g-table-wrap">'.$m[0].'</div>';
  },$content);
}
add_filter('the_content','a3g_responsive_tables',20);

function a3g_entity_related_post_ids($post_type){
  $entity_ids=get_posts([
    'post_type'=>$post_type,
    'post_status'=>'publish',
    'numberposts'=>-1,
    'fields'=>'ids',
    'no_found_rows'=>true,
  ]);
  $out=[];
  foreach($entity_ids as $entity_id){
    $raw=(string)get_post_meta($entity_id,'_a3_related_post_ids',true);
    foreach(preg_split('/[^0-9]+/',$raw) as $id){
      $id=(int)$id;if($id>0)$out[$id]=$id;
    }
  }
  return array_values($out);
}

function a3g_legacy_section($category_ids,$title,$subtitle='',$limit=12,$exclude=[],$link_category=0){
  $category_ids=array_values(array_filter(array_map('intval',(array)$category_ids)));
  if(!$category_ids)return false;
  $q=a3g_query([
    'category__in'=>$category_ids,
    'posts_per_page'=>(int)$limit,
    'post__not_in'=>array_values(array_filter(array_map('intval',(array)$exclude))),
  ]);
  if(!$q->have_posts())return false;
  $count=0;
  foreach($category_ids as $cat_id){
    $cat=get_category($cat_id);
    if($cat&&!is_wp_error($cat))$count+=(int)$cat->count;
  }
  if(!$link_category)$link_category=$category_ids[0];
  ?>
  <section class="g-legacy-bridge">
    <div class="g-section-head">
      <div><span>من مكتبة أعطال الحالية</span><h2><?php echo esc_html($title); ?></h2><?php if($subtitle): ?><p><?php echo esc_html($subtitle); ?></p><?php endif; ?></div>
      <div class="g-legacy-count"><?php echo esc_html(number_format_i18n($count)); ?> محتوى موجود بالفعل</div>
    </div>
    <div class="g-news-grid g-legacy-grid">
      <?php while($q->have_posts()):$q->the_post();a3g_card(get_the_ID(),'g-legacy-card');endwhile;wp_reset_postdata(); ?>
    </div>
    <div class="g-legacy-more"><a href="<?php echo esc_url(a3g_cat_link($link_category)); ?>">عرض كل المحتوى القديم المرتبط ←</a></div>
  </section>
  <?php
  return true;
}

function a3g_platform_link($post_type,$fallback='/'){
  $u=get_post_type_archive_link($post_type);
  return $u ?: home_url($fallback);
}
function a3g_term_names($post_id,$taxonomy){
  $terms=get_the_terms($post_id,$taxonomy);
  if(!$terms||is_wp_error($terms))return [];
  return array_values(array_map(static fn($t)=>$t->name,$terms));
}
function a3g_first_term($post_id,$taxonomy){
  $names=a3g_term_names($post_id,$taxonomy);
  return $names[0]??'';
}
function a3g_related_post_ids($post_id=0){
  $post_id=$post_id?:get_the_ID();
  $raw=(string)get_post_meta($post_id,'_a3_related_post_ids',true);
  return array_values(array_filter(array_map('absint',preg_split('/[^0-9]+/',$raw))));
}
function a3g_directory_status($post_id=0){
  $post_id=$post_id?:get_the_ID();
  $terms=get_the_terms($post_id,'a3_directory_status');
  if(!$terms||is_wp_error($terms))return null;
  return $terms[0]??null;
}
function a3g_platform_card($post_id=0){
  $post_id=$post_id?:get_the_ID();
  $type=get_post_type($post_id);
  $year=(string)get_post_meta($post_id,'_a3_year',true);
  $price=function_exists('a3cp_vehicle_price')?a3cp_vehicle_price($post_id):'';
  $brand=a3g_first_term($post_id,'a3_brand');
  ?>
  <article class="g-platform-card">
    <a class="g-platform-media" href="<?php echo esc_url(get_permalink($post_id)); ?>">
      <?php if(has_post_thumbnail($post_id)){echo get_the_post_thumbnail($post_id,'large',['loading'=>'lazy']);}else{echo '<span class="g-fallback">A3TAL</span>';} ?>
    </a>
    <div class="g-platform-body">
      <div class="g-platform-kickers"><?php if($brand): ?><span><?php echo esc_html($brand); ?></span><?php endif; ?><?php if($year): ?><span><?php echo esc_html($year); ?></span><?php endif; ?></div>
      <h3><a href="<?php echo esc_url(get_permalink($post_id)); ?>"><?php echo esc_html(get_the_title($post_id)); ?></a></h3>
      <?php if($price): ?><strong class="g-platform-price"><?php echo esc_html($price); ?></strong><?php endif; ?>
      <p><?php echo esc_html(a3g_excerpt($post_id,18)); ?></p>
      <a class="g-platform-more" href="<?php echo esc_url(get_permalink($post_id)); ?>">عرض التفاصيل ←</a>
    </div>
  </article>
  <?php
}


function a3g_platform_archive_seo(){
  if(is_post_type_archive('a3_showroom')){
    return [
      'short'=>'معارض السيارات في مصر',
      'title'=>'معارض السيارات في مصر | الفروع المعتمدة ودليل الشراء | أعطال.كوم',
      'desc'=>'دليل معارض السيارات في مصر: فروع معتمدة رسميًا، عناوين وأرقام ومواعيد ومصادر تحقق، مع أدلة الحجز وتجربة القيادة والاستلام والتقسيط.'
    ];
  }
  if(is_post_type_archive('a3_motorcycle')){
    return [
      'short'=>'الموتوسيكلات والسكوتر في مصر',
      'title'=>'الموتوسيكلات والسكوتر في مصر | الماركات والمواصفات والصيانة | أعطال.كوم',
      'desc'=>'دليل شامل للموتوسيكلات والسكوتر في مصر: TVS وBajaj والياباني والهندي والصيني، مواصفات ومقارنات وشراء وصيانة وقطع غيار وأعطال.'
    ];
  }
  return null;
}
add_filter('wpseo_title',function($title){$seo=a3g_platform_archive_seo();return $seo?$seo['title']:$title;},90);
add_filter('wpseo_metadesc',function($desc){$seo=a3g_platform_archive_seo();return $seo?$seo['desc']:$desc;},90);
add_filter('wpseo_opengraph_title',function($title){$seo=a3g_platform_archive_seo();return $seo?$seo['title']:$title;},90);
add_filter('wpseo_opengraph_desc',function($desc){$seo=a3g_platform_archive_seo();return $seo?$seo['desc']:$desc;},90);
add_filter('wpseo_twitter_title',function($title){$seo=a3g_platform_archive_seo();return $seo?$seo['title']:$title;},90);
add_filter('wpseo_twitter_description',function($desc){$seo=a3g_platform_archive_seo();return $seo?$seo['desc']:$desc;},90);
add_filter('document_title_parts',function($parts){
  $seo=a3g_platform_archive_seo();
  if($seo)$parts['title']=$seo['short']??$seo['title'];
  return $parts;
},90);


function a3g_showroom_social_image($image=''){
  if(is_singular('a3_showroom') && has_post_thumbnail()){
    $featured=get_the_post_thumbnail_url(get_queried_object_id(),'full');
    if($featured) return $featured;
  }
  if(is_post_type_archive('a3_showroom')){
    $ids=get_posts([
      'post_type'=>'attachment',
      'post_status'=>'inherit',
      'posts_per_page'=>1,
      'fields'=>'ids',
      'meta_key'=>'_a3_asset_key',
      'meta_value'=>'showroom-official-exterior-v2',
    ]);
    if($ids){
      $src=wp_get_attachment_image_url((int)$ids[0],'full');
      if($src) return $src;
    }
  }
  return $image;
}
add_filter('wpseo_opengraph_image','a3g_showroom_social_image',99);
add_filter('wpseo_twitter_image','a3g_showroom_social_image',99);

<?php
/** Focused regression checks for content ownership, summaries and query ordering. */
define('ABSPATH', __DIR__);
define('HOUR_IN_SECONDS', 3600);
$hooks=[];$cache=[];$is_admin=false;
$posts=[
  1=>(object)['ID'=>1,'post_type'=>'a3_dtc','post_status'=>'publish'],
  2=>(object)['ID'=>2,'post_type'=>'post','post_status'=>'publish'],
  3=>(object)['ID'=>3,'post_type'=>'a3_dtc','post_status'=>'publish'],
];
$links=[1=>2,3=>3];
$fields=[
  2=>['post_excerpt'=>'','post_content'=>'<aside><p>راجع P0430 في Bank 2 فقط.</p></aside><p>كود P0420 يعني أن كمبيوتر المحرك رصد كفاءة أقل من الحد المتوقع للمحول الحفاز في الجهة الأولى. لا يثبت الكود وحده أن حساس الأكسجين تالف، ويجب فحص الأسباب قبل تغيير أي قطعة.</p>'],
  3=>['post_excerpt'=>'شرح محفوظ كتبه فريق التحرير ويظل المرجع المستخدم في ملخص الصفحة.','post_content'=>''],
];
$guides=[
  (object)['ID'=>101,'post_title'=>'مراكز صيانة كيا المعتمدة في الدلتا','post_content'=>'عناوين طنطا والمنصورة','post_password'=>''],
  (object)['ID'=>102,'post_title'=>'توكيل MG في مصر','post_content'=>'خدمات القاهرة','post_password'=>''],
  (object)['ID'=>103,'post_title'=>'صيانة جيلي Emgrand','post_content'=>'خدمات مصر','post_password'=>''],
];
$terms=['kia'=>(object)['slug'=>'kia','name'=>'Kia'],'mg'=>(object)['slug'=>'mg','name'=>'MG']];
function add_action($n,$f,$p=10,$a=1){global $hooks;$hooks[$n][]=$f;}
function add_filter($n,$f,$p=10,$a=1){add_action($n,$f,$p,$a);}
function get_post_type($id){global $posts;return $posts[$id]->post_type??false;}
function get_post_status($id){global $posts;return $posts[$id]->post_status??false;}
function a3g_dtc_content_id($id){global $links;return $links[$id]??$id;}
function get_post_field($key,$id){global $fields;return $fields[$id][$key]??'';}
function wp_strip_all_tags($s){return strip_tags($s);}
function strip_shortcodes($s){return preg_replace('/\[[^\]]*\]/','',$s);}
function wp_trim_words($s,$n,$end='…'){$w=preg_split('/\s+/u',trim($s));return count($w)>$n?implode(' ',array_slice($w,0,$n)).$end:$s;}
function get_transient($k){global $cache;return $cache[$k]??false;}
function set_transient($k,$v,$time){global $cache;$cache[$k]=$v;}
function delete_transient($k){global $cache;unset($cache[$k]);}
function get_posts($args){global $posts,$guides;return ($args['post_type']??'')==='a3_dtc'?[$posts[1],$posts[3]]:$guides;}
function is_admin(){global $is_admin;return $is_admin;}
function absint($n){return abs((int)$n);}
function get_term_by($field,$value,$tax){global $terms;return $terms[$value]??false;}
function a3g_dtc_catalog(){return [['code'=>'P0420','id'=>1],['code'=>'P0136','id'=>3]];}
class Query {
  public $vars=['s'=>'P0420','post__not_in'=>[99]];
  function is_main_query(){return true;}
  function is_search(){return true;}
  function get($key){return $this->vars[$key]??null;}
  function set($key,$value){$this->vars[$key]=$value;}
}
function expect($ok,$message){if(!$ok)throw new RuntimeException($message);echo 'PASS '.$message."\n";}
require __DIR__.'/../theme-source/a3tal-global/ux-improvements-20261031.php';
expect(a3g_ux_original_guide_id(1)===2,'A mirrored code resolves to its published original');
expect(a3g_ux_original_guide_id(3)===3,'A unique code keeps its own page');
expect(a3g_ux_mirror_ids()===[1],'Only mirrored records are excluded');
$summary=a3g_ux_dtc_summary(2,'P0420');
expect(strpos($summary,'كود P0420 يعني')===0 && strpos($summary,'P0430')===false,'Quick answer starts with this code, not an unrelated notice');
expect(a3g_ux_dtc_summary(3,'P0136')===$fields[3]['post_excerpt'],'An editorial excerpt is preserved');
expect(a3g_ux_dtc_summary(999,'P9999')==='','Missing source content produces no invented answer');
expect(count(a3g_ux_directory_guides('kia'))===1,'English Kia term finds a published Arabic guide');
expect(count(a3g_ux_directory_guides('kia','طنطا'))===1,'City filter matches a city covered by the guide');
expect(count(a3g_ux_directory_guides('kia','أسوان'))===0,'A city absent from the guide returns no match');
expect(count(a3g_ux_directory_guides('mg'))===1,'MG does not match Emgrand by substring');
expect(a3g_ux_directory_guides('not-a-real-term')===[],'Unknown brands create no false matches');
$query=new Query();foreach($hooks['pre_get_posts'] as $callback)$callback($query);
expect($query->get('post__not_in')===[99,1],'Existing search exclusions are preserved');
expect($query->get('a3tal_ux_exact_code_id')===2,'Exact code prioritizes the original before pagination');
$wpdb=(object)['posts'=>'wp_posts'];$orderby='wp_posts.post_date DESC';foreach($hooks['posts_orderby'] as $callback)$orderby=$callback($orderby,$query);
expect(strpos($orderby,'CASE WHEN wp_posts.ID = 2 THEN 0 ELSE 1 END, wp_posts.post_date DESC')===0,'Exact-code ordering keeps the existing global ranking as tie breaker');
$is_admin=true;$admin_query=new Query();foreach($hooks['pre_get_posts'] as $callback)$callback($admin_query);
expect($admin_query->get('post__not_in')===[99],'Administrator searches remain unchanged');
echo "UX_REGRESSION_CHECKS_PASSED\n";

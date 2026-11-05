#!/usr/bin/env python3
"""Release researched general brake-clunk guide with safe bridge publication and live SEO checks."""
from pathlib import Path
import types
source_file=Path("scripts/publish-pseo-symptoms-20261105.py")
src=source_file.read_text("utf-8")
old='category_map={"عفشة":(11,"نظام التعليق"),'
new='category_map={"فرامل":(10,"مشاكل الفرامل"),"عفشة":(11,"نظام التعليق"),'
if src.count(old)!=1: raise RuntimeError("Guarded publishing template changed: refusing to patch category")
src=src.replace(old,new,1)
module=types.ModuleType("a3tal_brake_guarded_publisher")
module.__file__=str(source_file)
exec(compile(src,str(source_file),"exec"),module.__dict__)
original=Path("data/editorial/brake-clunk-first-stop-after-reversing-20261105.html").read_text("utf-8")
if original.count("<h2>الأسئلة الشائعة</h2>")!=1: raise RuntimeError("FAQ insertion marker changed")
staged=Path("/tmp/a3tal-brake-clunk-reverse-first-stop-20261105.html")
staged.write_text(original.replace("<h2>الأسئلة الشائعة</h2>","<h2>أسئلة شائعة</h2>",1),encoding="utf-8")
module.POSTS=[{
 "slug":"brake-clunk-first-stop-after-reversing-diagnosis",
 "file":str(staged),
 "title":"صوت طقة عند أول فرملة بعد الرجوع للخلف؟ الفرق بين حركة التيل وجلب المقص",
 "excerpt":"تسمع طقة من قدام أول ما تدوس فرامل بعد الرجوع للخلف؟ اعرف الفرق بين حركة تيل الفرامل والكاليبر وجلب المقص وقواعد الفتيس وكيف يفحصها الفني.",
 "focus":"صوت طقة أول فرملة بعد الرجوع للخلف",
 "category":"فرامل",
 "checks":["الرجوع للخلف","الكاليبر","{{a3tal_image:detail}}"],
 "dedup":["طقة أول فرملة بعد الرجوع","صوت فرامل تغيير الاتجاه"],
 "match":["طقة","فرملة","الرجوع"],
 "photo":[
   [("Brake pads.JPG","Amm105","CC BY-SA 3.0"),
    ("Rusty brake disc seen on a car located in a garage during the afternoon hours on a well-worn gravel surface.jpg","Shixart1985","CC BY 2.0")],
   [("Rusty brake disc seen on a car located in a garage during the afternoon hours on a well-worn gravel surface.jpg","Shixart1985","CC BY 2.0"),
    ("Brake shoe.jpg","Tiia Monto","CC BY-SA 4.0")]
 ],
 "alt":[
  "فني حقيقي يعرض تيل الفرامل لشرح احتمال الطقة عند أول فرملة بعد الرجوع للخلف",
  "قرص فرامل أمامي ظاهر في ورشة فعلية أثناء فحص محتمل لصوت الطقة عند تغيير اتجاه السير"
 ]
}]
if __name__=="__main__":
 module.main()
 print("A3TAL_BRAKE_CLUNK_NOV05_COMPLETE",flush=True)

"""
build_data.py — texts.csv ve detector_scores.csv uretimi (TEK KAYNAK)

Yeni veri geldikce METINLER ve SKORLAR listelerine satir eklenir,
betik calistirilir, CSV'ler bastan uretilir.

UZUNLUK KURALI (KARDEP Bolum 6.2 ve 10):
  ai metni  : 100-120 kelime bandi (kabul olcutu 110-120 hedeflenir)
  humanized : bant sarti YOK, yalnizca cikti uzunlugu kaydedilir
TABAN ETKISI:
  Ham ai metnine dedektor 0.00 verdiyse kacirma olculemez; "OLCULEMEZ" isaretlenir.
"""

import pandas as pd, os

METINLER = [
 dict(text_id="T001", label="ai", prompt_id=1, model="ChatGPT", humanizer="", source_text_id="",
  raw_text="Türkiye Cumhuriyeti, 29 Ekim 1923 tarihinde ilan edilmiş bağımsız ve demokratik bir devlettir. Ülkenin başkenti Ankara'dır ve devletin yönetim merkezi burada yer alır. Türkiye'nin yönetim biçimi cumhuriyettir. Cumhuriyet, egemenliğin millete ait olduğu ve vatandaşların yöneticilerini seçimler aracılığıyla belirlediği bir yönetim sistemidir. Bu sayede halk, ülkenin yönetiminde söz sahibi olur ve demokratik haklarını kullanabilir. Türkiye, hukuk devleti ilkelerine bağlı kalarak vatandaşlarının hak ve özgürlüklerini korumayı hedefler. Zengin tarihi, kültürel mirası ve doğal güzellikleriyle dikkat çeken Türkiye, farklı bölgeleri ve gelenekleriyle önemli bir ülkedir. Aynı zamanda eğitim, sağlık, ekonomi ve bilim alanlarında gelişimini sürdürerek geleceğe daha güçlü adımlarla ilerlemeyi amaçlamaktadır. Cumhuriyetin temel değerleri, birlik, beraberlik ve milli egemenlik anlayışını güçlendirerek toplumun ortak geleceğine katkı sağlar."),
 dict(text_id="T002", label="humanized", prompt_id=1, model="ChatGPT", humanizer="Aithor", source_text_id="T001",
  raw_text="Türkiye Cumhuriyeti, 29 Ekim 1923 tarihinde kurulan bağımsız ve demokratik bir devlettir. Ülkenin başkenti Ankara'dır ve yönetim merkezi de burada bulunmaktadır. Türkiye, yönetim biçimi olarak cumhuriyeti benimsemiştir. Cumhuriyet, egemenliğin millete ait olduğu ve halkın yöneticilerini seçimle belirlediği bir yönetim şeklidir. Bu sayede halk, ülke yönetiminde söz sahibi olur ve demokratik haklarını kullanabilir. Türkiye, hukuk devleti ilkesine bağlı kalarak vatandaşlarının hak ve özgürlüklerini korumayı amaçlamaktadır. Zengin tarihi, kültürel mirası ve doğal güzellikleriyle dikkat çeken Türkiye; farklı bölgeleriyle gelenekleriyle önemli bir ülkedir. Aynı zamanda eğitim sağlık ekonomi bilim alanlarında gelişimini sürdürerek geleceğe daha güçlü adımlarla ilerlemeyi hedeflemektedir. Cumhuriyetin temel değerleri birlik beraberlik milli egemenlik anlayışını güçlendirerek toplumun ortak geleceğine katkı sağlar."),
 dict(text_id="T003", label="humanized", prompt_id=1, model="ChatGPT", humanizer="Rephraser", source_text_id="T001",
  raw_text="Türkiye, 29 Ekim 1923'te kurulmuş egemen bir demokrasidir. Ankara, devlet yönetiminin bulunduğu ulus başkenti olarak hizmet vermektedir. Oradaki hükümet yapısı cumhuriyetçidir. Cumhuriyet, gücün, liderleri oylama yoluyla seçen halkın elinde olması anlamına gelir. Bu, vatandaşların arazinin işleyişini etkilemesine ve demokratik özgürlükleri uygulamasına olanak tanır. Devlet, hukuk kuralları ilkelerini takip ederek vatandaşların özgürlüklerini korumaya çalışır. Derin tarihi, kültürü ve doğasıyla tanınan Türkiye, farklı alan ve geleneklerde varlığını sürdürüyor. Eş zamanlı olarak eğitim, tıp, finans ve araştırma sektörlerinde ilerlemeyi ilerleterek daha iyi gelecekler planlamaktadır. Birlik, karşılıklı destek ve ulusal bağımsızlık gibi temel cumhuriyetçi idealleri güçlendirerek ortak toplumsal hedeflere yardımcı olur."),

 dict(text_id="T004", label="ai", prompt_id=2, model="ChatGPT", humanizer="", source_text_id="",
  raw_text="Madde doğada katı, sıvı ve gaz olmak üzere üç temel hâlde bulunur. Katı maddeler belirli bir şekle ve hacme sahiptir. Örneğin masa, taş ve kalem katı maddelere örnek olarak verilebilir. Sıvılar ise belirli bir hacme sahip olsalar da bulundukları kabın şeklini alırlar. Günlük hayatta içtiğimiz su, süt ve zeytinyağı sıvılara örnektir. Gazlar ise hem bulundukları kabın şeklini hem de hacmini alarak her yöne yayılır. Soluduğumuz hava ve mutfakta kullanılan doğalgaz buna örnek gösterilebilir. Bu hâller arasındaki temel fark, taneciklerin dizilişi ve hareket özgürlüğüdür. Katılarda tanecikler çok sıkı dururken, sıvılarda daha hareketli bir yapı görülür. Gazlarda ise tanecikler birbirinden oldukça uzaktır ve serbest şekilde hareket eder. Bu nedenle her hâl farklı özellikler gösterir."),
 dict(text_id="T005", label="humanized", prompt_id=2, model="ChatGPT", humanizer="Rephraser", source_text_id="T004",
  raw_text="Doğada madde üç temel biçimde bulunur: katı, sıvı ve gaz. Katıların sabit şekli ve hacmi vardır. Bir masa, bir taş ve bir kalem katı maddelere örnektir. Sıvılar belirli bir hacme sahiptirler ancak bulundukları kabın şeklini alırlar. Günlük olarak tükettiğimiz süt, su ve yemeklik yağ sıvıları temsil etmektedir. Bunun yerine gazlar, bulundukları kabın şekline ve boyutuna uygun olarak her yere dağılır. Soluduğumuz hava ve mutfak doğalgazı bu gibi durumları temsil ediyor. Temel ayrım, parçacık yerleşimi ve hareket özgürlüğünde yatmaktadır. Katı parçacıklar birbirine son derece yakın dururken, sıvılar daha fazla hareketlilik gösterir. Gaz parçacıkları birbirinden uzakta durur ve tamamen özgürce hareket eder. Sonuç olarak her durum benzersiz özellikler gösterir."),
 dict(text_id="T006", label="humanized", prompt_id=2, model="ChatGPT", humanizer="Aithor", source_text_id="T004",
  raw_text="Doğada madde üç temel hâlde bulunur: katı, sıvı ve gaz. Katıların şekli de hacmi de bellidir. Masa, taş ve kalem gibi nesneler bu gruba girer. Sıvılarda işler biraz değişir. Hacimleri sabit kalır ama içine kondukları kabın şeklini alırlar. Günlük hayatta içtiğimiz su, süt ve zeytinyağı sıvı hâle örnektir. Gazlar ise kabın hem şeklini hem de hacmini benimseyip her yöne yayılır; soluduğumuz hava ve mutfakta kullandığımız doğalgaz bu davranışı net biçimde gösterir. Peki bu hâller arasındaki temel fark ne? Cevap, taneciklerin dizilişinde ve hareket serbestliğinde saklı. Katı hâlde tanecikler sıkı sıkıya dizilmiştir. Sıvıya geçtiğimizde taneciklerin hareket alanı genişler. En serbest hâl ise gazdır. Tanecikler birbirinden iyice uzaklaşır ve neredeyse bağımsız hareket eder. Bu yüzden her hâlin kendine özgü özellikleri vardır."),

 dict(text_id="T007", label="ai", prompt_id=3, model="ChatGPT", humanizer="", source_text_id="",
  raw_text="Teknoloji, eğitim alanında hem önemli fırsatlar sunan hem de dikkatli kullanılmadığında bazı sorunlara yol açabilen bir araçtır. Bence doğru şekilde kullanıldığında öğrenmeyi daha kolay, eğlenceli ve verimli hâle getirir. İnternet sayesinde öğrenciler istedikleri bilgiye kısa sürede ulaşabilir, çevrim içi dersler izleyebilir ve farklı kaynaklardan yararlanabilir. Ayrıca akıllı tahta, tablet ve eğitim uygulamaları derslerin daha anlaşılır olmasına katkı sağlar. Ancak teknolojinin bilinçsiz kullanımı dikkat dağınıklığına neden olabilir ve öğrencilerin sosyal etkileşimini azaltabilir. Uzun süre ekran karşısında kalmak sağlık sorunlarına da yol açabilir. Bu nedenle teknolojinin eğitimde dengeli, amaçlı ve bilinçli kullanılması gerektiğini düşünüyorum. Böylece hem öğrenme süreci gelişir hem de öğrenciler bilgiye daha hızlı ulaşırken karşılaşabilecekleri olumsuz etkileri de en aza indirebilirler."),
 dict(text_id="T008", label="humanized", prompt_id=3, model="ChatGPT", humanizer="Aithor", source_text_id="T007",
  raw_text="Teknoloji, eğitim alanında hem büyük fırsatlar sunan hem de dikkatli kullanılmadığında bazı sorunlara yol açabilen bir araçtır. Bence doğru kullanıldığında öğrenmeyi daha kolay, eğlenceli ve verimli hale getirir. İnternet sayesinde öğrenciler istedikleri bilgiye kısa sürede ulaşabilir, online dersler izleyebilir ve farklı kaynaklardan yararlanabilir. Ayrıca akıllı tahta, tablet ve eğitim uygulamaları derslerin daha anlaşılır olmasına yardımcı olur. Ama teknolojinin yanlış kullanımı dikkat dağınıklığına yol açabilir ve öğrencilerin sosyal etkileşimini azaltır. Uzun süre ekran başında kalmak sağlık sorunlarına da neden olabilir. Bu yüzden teknolojinin eğitimde dengeli, amaçlı ve bilinçli kullanılması gerektiğini düşünüyorum. Böylece hem öğrenme süreci gelişir hem de öğrenciler bilgiye daha hızlı ulaşırken karşılaşabilecekleri olumsuz etkileri en aza indirebilirler."),
 dict(text_id="T009", label="humanized", prompt_id=3, model="ChatGPT", humanizer="Rephraser", source_text_id="T007",
  raw_text="Teknoloji, eğitimde önemli fırsatlar sunan ancak dikkatli kullanılmadığı takdirde sorunlara da yol açabilen bir araç olarak karşımıza çıkıyor. Doğru kullanıldığında öğrenmeyi daha kolay, daha keyifli ve daha verimli hale getirdiğine inanıyorum. İnternet sayesinde öğrenciler ihtiyaç duydukları bilgilere hızlı bir şekilde ulaşabilmekte, çevrimiçi dersleri izleyebilmekte ve çeşitli kaynaklardan yararlanabilmektedir. Ayrıca akıllı tahtalar, tabletler ve eğitim uygulamaları derslerin anlaşılmasını kolaylaştırmaya yardımcı olur. Ancak teknolojiyi düşünmeden kullanmak öğrencilerin dikkatini dağıtabilir ve sosyal etkileşimlerini azaltabilir. Ekran karşısında uzun süre vakit geçirmek de sağlık sorunlarına yol açabiliyor. Bu nedenle teknolojinin eğitimde dengeli, amaçlı ve bilinçli kullanılması gerektiğine inanıyorum. Bu yaklaşım, öğrenme sürecini geliştirerek öğrencilerin bilgiye daha hızlı erişmesine olanak tanırken olası olumsuz etkileri de azaltır."),

 dict(text_id="T010", label="ai", prompt_id=4, model="ChatGPT", humanizer="", source_text_id="",
  raw_text="Bir öğrencinin sınava etkili şekilde hazırlanması için öncelikle sınavın kapsamını, konularını ve soru türlerini ayrıntılı biçimde öğrenmesi gerekir. Daha sonra gerçekçi bir çalışma programı hazırlayarak konuları günlere dengeli şekilde bölmeli ve bu plana düzenli olarak uymalıdır. Çalışırken yalnızca ders okumak yerine not çıkarmak, önemli bilgileri tekrar etmek, farklı kaynaklardan soru çözmek ve eksiklerini belirlemek öğrenmeyi daha kalıcı hâle getirir. Anlamadığı konuları öğretmenine, arkadaşlarına veya güvenilir eğitim kaynaklarına danışarak tamamlaması büyük önem taşır. Belirli aralıklarla deneme sınavı çözerek zaman yönetimini geliştirmeli, yaptığı yanlışları dikkatlice incelemeli ve eksik olduğu konular üzerinde tekrar çalışmalıdır. Sınavdan önce düzenli uyumalı, sağlıklı beslenmeli, stresini kontrol etmeli, kendine güvenmeli ve sınava sakin, planlı, motive, dikkatli ve kararlı bir şekilde girmelidir."),
 dict(text_id="T011", label="humanized", prompt_id=4, model="ChatGPT", humanizer="Aithor", source_text_id="T010",
  raw_text="Bir öğrencinin sınava hazırlıkta ilk yapması gereken şey, sınavın kapsamını ve hangi konulardan sorumlu olduğunu ayrıntılı biçimde öğrenmek. Ardından gerçekçi bir çalışma programı hazırlayıp konuları günlere bölmeli ve bu plana düzenli uymalı. Çalışırken yalnızca okumak yetmez; not çıkarmak, önemli bilgilerin altını çizmek, tekrar yapmak ve bol soru çözmek öğrenmeyi kalıcı hâle getirir. Anlamadığı konularda öğretmenine, arkadaşlarına ya da güvenilir kaynaklara danışıp eksiklerini tamamlaması da bir o kadar önemli. Deneme sınavlarını belirli aralıklarla çözmek zaman yönetimini geliştirir. Yanlış yaptığı soruları dikkatle incelemeli, eksik kalan konulara yeniden dönmeli. Son günlerde yeni konu öğrenmek yerine genel tekrar yapmak, yeterince uyumak, dengeli beslenmek ve moralini yüksek tutmak en doğrusu. Böylece öğrenci, sınava kendine güvenerek girer."),
 dict(text_id="T012", label="humanized", prompt_id=4, model="ChatGPT", humanizer="Rephraser", source_text_id="T010",
  raw_text="Sınava etkili bir şekilde hazırlanabilmek için öğrencinin öncelikle sınavın kapsamını, konularını ve soru türlerini detaylı bir şekilde öğrenmesi gerekir. Daha sonra gerçekçi bir çalışma programı oluşturun, konularınızı günlere eşit olarak bölün ve bu plana tutarlı bir şekilde sadık kalın. Öğrenmeyi daha kalıcı hale getirmek, derslerde not almayı, önemli bilgileri tekrarlamayı, çeşitli kaynaklardan soru çözmeyi ve geliştirilecek alanları belirlemeyi içerir. Anlamadığı konuları öğretmeninden, arkadaşlarından veya güvendiği eğitim kaynaklarından yardım isteyerek bitirmesi onun için çok önemlidir. Düzenli olarak deneme sınavlarına girerek, hataları dikkatle gözden geçirerek ve zayıf konuları yeniden çalışarak zaman yönetimini geliştirmelidir. Sınavdan önce iyi uyumalı, sağlıklı beslenmeli, stresinizi yönetmeli, kendinize güvenmeli, sakin, planlı, motivasyonlu, dikkatli ve kararlı bir şekilde sınava girmelisiniz."),

 dict(text_id="T013", label="ai", prompt_id=5, model="ChatGPT", humanizer="", source_text_id="",
  raw_text="Yüz yüze eğitim ile uzaktan eğitimin kendine özgü avantajları ve dezavantajları vardır. Yüz yüze eğitimde öğrenciler öğretmenleriyle doğrudan iletişim kurabildiği için anlamadıkları konuları daha kolay sorabilir ve sınıf ortamında arkadaşlarıyla etkileşim içinde öğrenebilir. Bu durum motivasyonu artırırken düzenli çalışma alışkanlığı kazanmaya da yardımcı olur. Ancak ulaşım, zaman kaybı ve bazı ek masraflar yüz yüze eğitimin olumsuz yönleri arasında yer alır. Uzaktan eğitim ise istenilen yerden derslere katılma, zamandan tasarruf etme ve ders kayıtlarını tekrar izleyebilme açısından önemli kolaylık sağlar. Buna rağmen internet bağlantısı sorunları, dikkat dağınıklığı ve sosyal etkileşimin azalması öğrenmeyi olumsuz etkileyebilir. Bana göre hangi eğitim yönteminin daha başarılı olacağı, öğrencinin ihtiyaçlarına, çalışma düzenine, dersin özelliklerine ve teknolojik imkânlarına bağlı olarak değişebilir."),
 dict(text_id="T014", label="humanized", prompt_id=5, model="ChatGPT", humanizer="Aithor", source_text_id="T013",
  raw_text="Her iki eğitim modelinin de kendine göre güçlü ve zayıf yanları var. Sınıf ortamında öğrenciler öğretmenlerine doğrudan soru sorabiliyor, anlamadıkları konuyu oracıkta açıklatabiliyor. Arkadaşlarıyla etkileşim içinde öğrenmek motivasyonu yükseltiyor ve düzenli çalışma alışkanlığını destekliyor. Fakat her gün okula gidip gelmek ciddi bir zaman kaybı. Ulaşım masrafı, yemek ve kırtasiye gibi ek giderler de cabası. Uzaktan eğitimde ise durum farklı; derse nereden katılacağınıza kendiniz karar veriyor, kayıtları tekrar tekrar izleyebiliyor ve böylece ciddi oranda zaman tasarrufu sağlıyorsunuz. Öte yandan internet bağlantısı koptuğunda ya da dikkat dağınıklığı baş gösterdiğinde süreç aksayabiliyor. Sosyal etkileşimin azalması da işin bir başka olumsuz boyutu. Bana kalırsa hangi yöntemin daha başarılı olacağı öğrencinin ihtiyaçlarına, çalışma düzenine, dersin özelliklerine ve teknolojik imkânlarına göre değişir."),
 dict(text_id="T015", label="humanized", prompt_id=5, model="ChatGPT", humanizer="Rephraser", source_text_id="T013",
  raw_text="Hem yüz yüze hem de uzaktan eğitimin kendine göre artıları ve eksileri var. Yüz yüze eğitimde öğrenciler, öğretmenleriyle doğrudan iletişim kurarak belirsiz konuları kolayca sorabilir ve sınıf arkadaşlarıyla etkileşime girerek öğrenebilirler. Bu motivasyonu artırsa da tutarlı çalışma alışkanlıklarının oluşturulmasına da yardımcı olur. Ancak yüz yüze eğitimin ulaşım, zaman kaybı ve ekstra maliyet gibi dezavantajları da bulunmaktadır. Öte yandan uzaktan eğitim, derslere her yerden katılım olanağı sağlaması, zaman tasarrufu sağlaması ve öğrencilerin ders kayıtlarını tekrar izleyebilmelerine olanak sağlamasıyla büyük kolaylık sağlıyor. Ancak zayıf internet bağlantıları, dikkat dağıtıcı unsurlar ve sosyal etkileşimin azalması gibi sorunlar öğrenme sürecine zarar verebilir. Bana göre en etkili eğitim yöntemi öğrencinin ihtiyaçlarına, programına, dersin özelliklerine ve mevcut teknolojiye bağlıdır."),

 dict(text_id="T016", label="ai", prompt_id=1, model="Gemini", humanizer="", source_text_id="",
  raw_text="Türkiye Cumhuriyeti, Asya ve Avrupa kıtalarını birbirine bağlayan oldukça stratejik bir konuma sahip, köklü bir geçmişe dayanan bağımsız ve modern bir devlettir. Ülkenin başkenti Ankara'dır ve burası siyasi ile idari kararların alındığı en önemli merkez konumundadır. Türkiye'nin yönetim biçimi cumhuriyettir. Cumhuriyet kavramı, egemenliğin kayıtsız ve şartsız bir biçimde tamamen millete ait olduğu, devleti yönetecek kişilerin doğrudan halk tarafından belirli bir süre için serbest seçimlerle iş başına getirildiği adil bir sistemi ifade eder. Bu sistemde hukukun üstünlüğü ve tüm vatandaşların eşit haklara sahip olması en temel prensiplerdendir. Ülkemizde bu demokratik yapı, halkın kendi hür iradesini doğrudan sandığa yansıtmasıyla güvence altına alınmıştır ve devletin tüm kurumları bu demokratik temel üzerinde titizlikle şekillenerek daima halkı için çalışır."),

 dict(text_id="T017", label="humanized", prompt_id=1, model="Gemini", humanizer="Aithor", source_text_id="T016",
  raw_text="Türkiye Cumhuriyeti, Asya ve Avrupa kıtalarını birbirine bağlayan çok stratejik bir konuma sahip, köklü bir geçmişe dayanan bağımsız ve modern bir devlettir. Ülkenin başkenti Ankara'dır ve burası siyasi ile idari kararların alındığı en önemli merkez konumundadır. Türkiye'nin yönetim biçimi cumhuriyettir. Cumhuriyet kavramı, egemenliğin kayıtsız ve şartsız bir biçimde tamamen millete ait olduğu, devleti yönetecek kişilerin doğrudan halk tarafından belirli bir süre için serbest seçimlerle iş başına getirildiği adil bir sistemi ifade eder. Bu sistemde hukukun üstünlüğü ve tüm vatandaşların eşit haklara sahip olması en temel prensiplerdendir. Ülkemizde bu demokratik yapı, halkın kendi hür iradesini doğrudan sandığa yansıtmasıyla güvence altına alınmıştır ve devletin tüm kurumları bu demokratik temel üzerinde titizlikle şekillenerek daima halkı için çalışır."),

 dict(text_id="T018", label="humanized", prompt_id=1, model="Gemini", humanizer="Rephraser", source_text_id="T016",
  raw_text="Türkiye Cumhuriyeti, Asya ve Avrupa kıtalarını birbirine bağlayan son derece stratejik bir konuma sahip, köklü bir geçmişe dayanan bağımsız ve çağdaş bir devlettir. Ülkenin başkenti Ankara olup, siyasi ve idari kararların alındığı en önemli merkezdir. Türkiye'nin yönetim şekli cumhuriyettir. Cumhuriyet kavramı, egemenliğin kayıtsız şartsız ve kayıtsız şartsız tamamen millete ait olduğu, devleti yönetecek olanların doğrudan halk tarafından belirli bir süre için serbest seçimlerle seçildiği adil sistemi ifade eder. Bu sistemde hukukun üstünlüğü ve tüm vatandaşların eşit haklara sahip olması en temel ilkelerdir. Ülkemizde bu demokratik yapı, halkın özgür iradesinin doğrudan sandıkta yansımasıyla sağlanır ve devletin tüm kurumları bu demokratik temel üzerinde titizlikle şekillendirilir ve daima halk için çalışır."),

 dict(text_id="T019", label="ai", prompt_id=2, model="Gemini", humanizer="", source_text_id="",
  raw_text="Maddenin temel olarak katı, sıvı, gaz ve plazma olmak üzere doğada dört farklı hâli bulunmaktadır. Katı hâlde maddenin belirli bir şekli ve sabit hacmi vardır; tanecikler birbirine çok sıkı bağlıdır. Günlük yaşamımızdan masa veya buz katılara iyi birer örnektir. Sıvı hâlde ise maddenin belirli bir hacmi varken, bulundukları kabın şeklini alırlar ve tanecikleri kayarak yer değiştirir. İçtiğimiz su sıvılara güzel bir örnektir. Gaz hâlindeki maddelerin belirli bir şekli veya hacmi yoktur; tanecikler serbestçe hareket ederek ortamı tamamen kaplarlar. Soluduğumuz hava veya su buharı gazdır. Son olarak plazma hâli, yüksek enerjili iyonize olmuş gazları temsil eder ve florasan lambalarda açıkça görülür. Bu hâller birbirinden genel olarak tanecikler arasındaki boşluk, etkileşim kuvveti ve hareket serbestliği boyutunda farklılaşır."),

 dict(text_id="T020", label="humanized", prompt_id=2, model="Gemini", humanizer="Aithor", source_text_id="T019",
  raw_text="Maddenin doğada katı, sıvı, gaz ve plazma olmak üzere dört temel hali vardır. Katı halde maddenin belirli bir şekli ve sabit hacmi bulunur; tanecikler birbirine çok sıkı bağlıdır. Günlük yaşamdan masa veya buz katılara iyi birer örnektir. Sıvı halde ise maddenin belirli bir hacmi varken bulundukları kabın şeklini alırlar ve tanecikleri kayarak yer değiştirir. İçtiğimiz su sıvılara güzel bir örnektir. Gaz halindeki maddelerin belirli bir şekli veya hacmi yoktur; tanecikler serbestçe hareket ederek ortamı tamamen kaplarlar. Soluduğumuz hava veya su buharı gazdır. Son olarak plazma hali yüksek enerjili iyonize olmuş gazları temsil eder ve florasan lambalarda açıkça görülür. Bu haller birbirinden genel olarak tanecikler arasındaki boşluk etkileşim kuvveti ve hareket serbestliği boyutunda farklılaşır."),

 dict(text_id="T021", label="humanized", prompt_id=2, model="Gemini", humanizer="Rephraser", source_text_id="T019",
  raw_text="Doğada esas olarak maddenin dört farklı hali vardır: katı, sıvı, gaz ve plazma. Bir katıda madde, parçacıkları çok sıkı bir şekilde bir arada tutulduğu için belirli bir şekli ve sabit bir hacmi korur. Günlük hayatımızdaki sofra tuzu ve buz katı maddelere güzel bir örnektir. Sıvı halde sabit hacimli bir madde bulunduğu kabın şeklini alacak ve parçacıkları birbirinin üzerinden kayarak konum değiştirecektir. İçtiğimiz su sıvıya harika bir örnektir. Gaz halindeki maddelerin belirli bir şekli veya hacmi yoktur, çünkü parçacıkları serbestçe hareket eder ve kabın tamamını dolduracak şekilde yayılır. Soluduğumuz hava veya su buharı bir gazdır. Son olarak, plazma durumu yüksek enerjili iyonize gazları temsil eder ve floresan lambalarda açıkça görülebilir. Bu durumlar genellikle parçacıklar arasındaki boşluk, etkileşim kuvveti ve hareket özgürlüğü açısından birbirlerinden farklılık gösterir."),

 dict(text_id="T022", label="ai", prompt_id=3, model="Gemini", humanizer="", source_text_id="",
  raw_text="Teknolojinin eğitim dünyasına entegre olması, fırsatları ve zorlukları beraberinde getiren karmaşık bir dönüşümdür. Olumlu yönden bakıldığında, bilgiye erişim hızı artmış ve öğrenme mekandan bağımsız hale gelmiştir. Öğrenciler zengin dijital kaynaklar, simülasyonlar ve uzaktan eğitim platformları sayesinde kendi hızlarında kişiselleştirilmiş bir öğrenme deneyimi yaşayabilmektedir. Ancak bu durumun bir de karanlık yüzü vardır. Ekran başında geçirilen sürenin artması, dikkat dağınıklığı ve odaklanma problemlerini tetikleyebilmektedir. Ayrıca, teknolojiye eşit erişememe sorunu, öğrenciler arasındaki eğitimde fırsat eşitsizliğini daha da derinleştirme potansiyeline sahiptir. Sosyal izolasyon ile teknolojiye aşırı bağımlılık eleştirel düşünme becerilerini de köreltebilir. Sonuç olarak, teknolojiyi tamamen reddetmek yerine onu bilinçli, dengeyi koruyan ve pedagojik hedeflere hizmet eden değerli bir araç olarak kullanmak temel hedefimiz olmalıdır."),

 dict(text_id="T023", label="humanized", prompt_id=3, model="Gemini", humanizer="Aithor", source_text_id="T022",
  raw_text="Teknolojinin eğitim dünyasına girmesi, fırsatlar ve zorluklar getiren karmaşık bir değişimdir. İyi tarafından bakarsak, bilgiye ulaşma hızı artmış ve öğrenme yerden bağımsız hale gelmiştir. Öğrenciler zengin dijital kaynaklar, simülasyonlar ve uzaktan eğitim platformları sayesinde kendi hızlarında kişiselleştirilmiş bir öğrenme deneyimi yaşayabilmektedir. Ama bunun bir de karanlık yüzü vardır. Ekran başında geçirilen zamanın artması dikkat dağınıklığı ve odaklanma problemlerini tetikleyebilir. Ayrıca teknolojiye eşit erişememe sorunu öğrenciler arasındaki eğitimde fırsat eşitsizliğini daha da derinleştirme potansiyeline sahiptir. Sosyal izolasyonla teknolojiye aşırı bağımlılık eleştirel düşünme becerilerini de köreltebilir. Sonuç olarak, teknolojiyi tamamen reddetmek yerine onu bilinçli, dengeyi koruyan ve pedagojik hedeflere hizmet eden değerli bir araç olarak kullanmak temel hedefimiz olmalıdır."),

 dict(text_id="T024", label="humanized", prompt_id=3, model="Gemini", humanizer="Rephraser", source_text_id="T022",
  raw_text="Teknolojiyi eğitime getirmek, hem fırsatlar hem de zorluklar sunan karmaşık bir değişimdir. Olumlu tarafı, bilgiye erişim daha hızlı hale geldi ve öğrenme artık belirli bir konuma bağlı değil. Zengin dijital kaynaklar, simülasyonlar ve uzaktan eğitim platformları sayesinde öğrenciler kendi hızlarında kişiselleştirilmiş bir öğrenme deneyiminin keyfini çıkarabilirler. Ancak bu durumun bir de dezavantajı var. Ekran karşısında daha fazla vakit geçirmek dikkatin dağılmasına ve odaklanma sorunlarına yol açabilir. Ek olarak, teknolojiye eşit erişim eksikliği, öğrencilere yönelik eğitim fırsatları arasındaki açığı daha da genişletebilir. Sosyal izolasyon ve teknolojiye aşırı bağımlılık da eleştirel düşünme yeteneklerini köreltebilir. Bu nedenle teknolojiyi tamamen bir kenara bırakmak yerine, onu bilinçli, dengeli ve pedagojik açıdan etkili bir kaynak olarak kullanmak öncelikli hedefimiz olmalıdır."),

 dict(text_id="T025", label="ai", prompt_id=4, model="Gemini", humanizer="", source_text_id="",
  raw_text="Bir öğrencinin sınava oldukça etkili ve kalıcı bir şekilde hazırlanması için ilk olarak kapsamlı, gerçekçi bir çalışma planı oluşturması gerekir. Hangi konuların ağırlıklı olduğuna karar vererek kısıtlı zamanını mantıklı bir biçimde dağıtmalıdır. İkinci adımda, güncel ders notları, kitaplar ve geçmiş sınav soruları gibi gerekli bütün materyalleri eksiksiz bir biçimde çalışma masasında bir araya getirmelidir. Ardından, sadece okumak yerine kendi cümleleriyle özetler çıkararak veya kavram haritaları çizerek aktif bir öğrenme süreci yürütmelidir. Konular tamamlandıkça, gerçek sınav ortamını simüle eden deneme sınavları çözerek hem zaman yönetimini geliştirmeli hem de bilgi eksiklerini tespit ederek bu zayıf alanlara tekrar odaklanmalıdır. Son olarak, sınavdan hemen önceki günlerde yoğun çalışmayı bırakıp tamamen zihinsel dinlenmeye önem vererek stresi yönetmelidir."),

 dict(text_id="T026", label="humanized", prompt_id=4, model="Gemini", humanizer="Aithor", source_text_id="T025",
  raw_text="Bir öğrencinin sınava etkili ve kalıcı bir şekilde hazırlanabilmesi için öncelikle kapsamlı, gerçekçi bir çalışma planı yapması gerekir. Hangi konuların ağırlıklı olduğuna karar vererek kısıtlı zamanını mantıklı bir şekilde dağıtmalıdır. İkinci adımda, güncel ders notları, kitaplar ve geçmiş sınav soruları gibi gerekli tüm materyalleri eksiksiz bir şekilde çalışma masasında toplamalıdır. Daha sonra, sadece okumak yerine kendi cümleleriyle özetler çıkararak ya da kavram haritaları çizerek aktif bir öğrenme süreci yürütmelidir. Konular tamamlandıkça, gerçek sınav ortamını simüle eden deneme sınavları çözerek hem zaman yönetimini geliştirmeli hem de bilgi eksiklerini tespit ederek bu zayıf alanlara tekrar odaklanmalıdır. En son olarak da sınavdan hemen önceki günlerde yoğun çalışmayı bırakıp tamamen zihinsel dinlenmeye önem vererek stresi yönetmelidir."),

 dict(text_id="T027", label="humanized", prompt_id=4, model="Gemini", humanizer="Rephraser", source_text_id="T025",
  raw_text="Sınava etkili ve kalıcı bir şekilde hazırlanabilmek için öncelikle öğrencinin kapsamlı ve gerçekçi bir çalışma planı geliştirmesi gerekir. Hangi konuların en önemli olduğuna karar vererek sınırlı zamanını akıllıca ayırmalıdır. İkinci adımda güncel ders notları, kitaplar, geçmiş sınav soruları gibi gerekli tüm materyalleri çalışma masanızda eksiksiz bir şekilde toplayın. Daha sonra sadece okumak yerine konuyu kendi cümleleriyle özetleyerek veya kavram haritaları oluşturarak aktif öğrenmeye girişmelidir. Konuları bitirdikçe gerçek sınav ortamını taklit eden deneme sınavlarına girerek, bilgi eksikliklerinizi tespit ederek ve yine o zayıf alanlara odaklanarak zaman yönetiminizi geliştirmelisiniz. Son olarak, sınavdan hemen önceki günlerde yoğun çalışmaya ara vererek ve tam bir zihinsel dinlenmeye odaklanarak stresi yönetmelisiniz."),

 dict(text_id="T028", label="ai", prompt_id=5, model="Gemini", humanizer="", source_text_id="",
  raw_text="Yüz yüze eğitim ile uzaktan eğitim, günümüzde farklı deneyimlerle öne çıkar. Yüz yüze eğitimin en belirgin avantajı, öğretmen ve öğrenciler arasındaki canlı etkileşim sayesinde sosyalleşmeyi, grup çalışmalarını ve anında geri bildirimi desteklemesidir. Ancak belirli bir mekana ve katı bir zaman çizelgesine bağlı kalma zorunluluğu, ulaşım gibi ek maliyetler yaratması açısından dezavantajlıdır. Diğer yandan, uzaktan eğitim zaman ve mekandan tamamen bağımsız olmasıyla öğrencilere muazzam bir esneklik sunar; bireyler diledikleri yerden katılım sağlayarak ciddi bir maliyet tasarrufu elde ederler. Buna karşın, ekran başında geçirilen sürenin yarattığı odaklanma sorunları, aniden gelişebilecek altyapısal veya teknik aksaklıklar ve en önemlisi sosyal izolasyon, uzaktan eğitimin temel dezavantajları olarak görülmektedir. Her iki model de kendi içinde değerli fırsatlar barındırır."),

 dict(text_id="T029", label="humanized", prompt_id=5, model="Gemini", humanizer="Aithor", source_text_id="T028",
  raw_text="Yüz yüze eğitim ve uzaktan eğitim, günümüzde farklı deneyimlerle öne çıkar. Yüz yüze eğitimin en belirgin avantajı, öğretmen ve öğrenciler arasındaki canlı etkileşim sayesinde sosyalleşmeyi, grup çalışmalarını ve anında geri bildirimi desteklemesidir. Ancak belirli bir mekana ve katı bir zaman çizelgesine bağlı kalma zorunluluğu ulaşım gibi ek maliyetler yaratması açısından dezavantajlıdır. Diğer yandan uzaktan eğitim zaman ve mekandan tamamen bağımsız olmasıyla öğrencilere muazzam bir esneklik sunar bireyler diledikleri yerden katılım sağlayarak ciddi bir maliyet tasarrufu elde ederler. Buna karşın ekran başında geçirilen sürenin yarattığı odaklanma sorunları aniden gelişebilecek altyapısal veya teknik aksaklıklar ve en önemlisi sosyal izolasyon uzaktan eğitimin temel dezavantajları olarak görülmektedir. Her iki model de kendi içinde değerli fırsatlar barındırır."),

 dict(text_id="T030", label="humanized", prompt_id=5, model="Gemini", humanizer="Rephraser", source_text_id="T028",
  raw_text="Günümüzde yüz yüze ve uzaktan eğitim farklı deneyimler sunmaktadır. Yüz yüze öğrenmenin en belirgin faydası sosyalleşmeyi, takım çalışmasını ve öğretmenler ile öğrenciler arasındaki gerçek zamanlı etkileşim yoluyla anında geri bildirimi teşvik etmesidir. Ancak belirli bir yere bağlı olmak ve katı bir programa bağlı olmak, ulaşım maliyetleri gibi ekstra harcamalara yol açması nedeniyle bir dezavantajdır. Öte yandan uzaktan eğitim, öğrencilere zaman ve mekandan bağımsız olarak öğrenme olanağı sağlayarak büyük bir esneklik sağlayarak bireylerin istedikleri yerden eğitim alarak maliyetlerden önemli ölçüde tasarruf etmelerini sağlar. Buna karşılık, uzaktan eğitimin başlıca dezavantajları ise ekran kullanımından kaynaklanan dikkat sorunları, beklenmeyen teknik veya altyapı arızaları ve en önemlisi sosyal izolasyon olarak tanımlanmaktadır. Her iki modelin de kendi içinde değerli bir potansiyeli var."),

 dict(text_id="T031", label="ai", prompt_id=1, model="Claude", humanizer="", source_text_id="",
  raw_text="Türkiye Cumhuriyeti, Asya ve Avrupa kıtaları arasında yer alan, üç tarafı denizlerle çevrili bir ülkedir. 29 Ekim 1923 tarihinde Mustafa Kemal Atatürk önderliğinde kurulmuş ve başkenti Ankara olarak belirlenmiştir. Ülkenin yönetim biçimi cumhuriyettir; 2018 yılından itibaren cumhurbaşkanlığı hükûmet sistemiyle yönetilmektedir. Cumhuriyet, egemenliğin belirli bir kişiye ya da aileye değil, doğrudan halka ait olduğu yönetim biçimidir. Bu düzende halk, belirli aralıklarla yapılan seçimlerle kendisini yönetecek temsilcileri özgürce seçer ve yöneticiler halka karşı sorumludur. Yasama görevini Türkiye Büyük Millet Meclisi yürütür. Resmî dili Türkçe, para birimi Türk lirasıdır. Nüfusu 85 milyonun üzerindedir ve İstanbul en kalabalık şehridir. Anayasaya göre Türkiye demokratik, laik ve sosyal bir hukuk devletidir; bayrağı ise kırmızı zemin üzerine ay yıldızdan oluşur."),

 dict(text_id="T032", label="humanized", prompt_id=1, model="Claude", humanizer="Aithor", source_text_id="T031",
  raw_text="Türkiye Cumhuriyeti, Asya ve Avrupa kıtaları arasında yer alan, üç tarafı denizlerle çevrili bir ülkedir. 29 Ekim 1923 tarihinde Mustafa Kemal Atatürk önderliğinde kurulmuş ve başkenti Ankara olarak belirlenmiştir. Ülkenin yönetim biçimi cumhuriyettir; 2018 yılından itibaren cumhurbaşkanlığı hükûmet sistemiyle yönetilmektedir. Cumhuriyet, egemenliğin belirli bir kişiye ya da aileye değil, doğrudan halka ait olduğu yönetim biçimidir. Bu düzende halk, belirli aralıklarla yapılan seçimlerle kendisini yönetecek temsilcileri özgürce seçer ve yöneticiler halka karşı sorumludur. Yasama görevini Türkiye Büyük Millet Meclisi yürütür. Resmî dili Türkçe, para birimi Türk lirasıdır. Nüfusu 85 milyonun üzerindedir ve İstanbul en kalabalık şehridir. Anayasaya göre Türkiye demokratik, laik ve sosyal bir hukuk devletidir; bayrağı ise kırmızı zemin üzerine ay yıldızdan oluşur."),

 dict(text_id="T033", label="humanized", prompt_id=1, model="Claude", humanizer="Rephraser", source_text_id="T031",
  raw_text="Türkiye, Asya ile Avrupa arasında yer alan, topraklarının üç tarafı denizlerle çevrili bir ülkedir. 29 Ekim 1923'te Mustafa Kemal Atatürk'ün önderliğinde Ankara başkent olmak üzere kuruldu. Ülke, 2018 yılından bu yana başkanlık sistemiyle faaliyet gösteren bir cumhuriyettir. Cumhuriyet, tek bir kişinin veya ailenin değil, iktidarın doğrudan halkın elinde olduğu yönetim türüdür. Bu sistemde insanlar, kendilerini yönetecek temsilcilerini düzenli seçimlerle özgürce seçerler ve yöneticiler halka karşı sorumludurlar. Türkiye Büyük Millet Meclisi yasama görevlerini yürütmekle sorumludur. Resmi dili Türkçe, para birimi ise Türk Lirasıdır. Nüfusu 85 milyonun üzerinde olup en büyük şehri İstanbul'dur. Anayasa'da Türkiye'nin demokratik, laik ve sosyal bir hukuk devleti olduğu belirtiliyor ve bayrağında kırmızı zemin üzerine ay-yıldız bulunuyor."),

 dict(text_id="T034", label="ai", prompt_id=2, model="Claude", humanizer="", source_text_id="",
  raw_text="Madde, doğada temel olarak katı, sıvı ve gaz hâlinde bulunur. Katı hâlde tanecikler birbirine çok yakındır ve düzenli biçimde titreşir; bu yüzden katıların belirli bir şekli ve hacmi vardır, örneğin buzdolabındaki buz küpü veya masamızın üzerindeki tahta kalem. Sıvı hâlde tanecikler arasındaki boşluk biraz artar, tanecikler birbiri üzerinden kayabilir; böylece sıvılar bulundukları kabın şeklini alır ama hacimleri değişmez, bardağa doldurduğumuz su bunun güzel bir örneğidir. Gaz hâlinde ise tanecikler çok uzak ve serbesttir, her yöne dağılırlar; bu nedenle gazların belirli bir şekli ve hacmi yoktur, mutfak tüpündeki doğal gaz ya da soluduğumuz hava buna örnektir. Bu hâller arasındaki temel fark, tanecikler arasındaki çekim kuvveti, uzaklık ve hareket serbestliğidir. Isı alışverişiyle madde bir hâlden diğerine geçebilir."),

 dict(text_id="T035", label="humanized", prompt_id=2, model="Claude", humanizer="Rephraser", source_text_id="T034",
  raw_text="Madde doğal olarak üç halde bulunur: katı, sıvı ve gaz. Bir katıda, parçacıklar birbirine sıkı bir şekilde paketlenir ve yerinde titreşir; bu nedenle katılar, buzdolabındaki buz küpü veya masanın üzerindeki tahta kalem gibi sabit bir şekil ve hacmi korur. Sıvı halde parçacıklar arasındaki boşluk hafifçe artarak onların birbirlerinin üzerinden kaymalarına olanak tanır; bu nedenle sıvılar sabit bir hacmi korurken bulundukları kabın şekline uyarlar. Bir bardağa döktüğümüz su buna çok güzel bir örnektir. Gaz halinde parçacıklar birbirinden çok uzaktadır ve her yöne serbestçe hareket eder; dolayısıyla gazların, mutfak tüplerinde depolanan doğalgazda veya soluduğumuz havada olduğu gibi belirli bir şekli veya hacmi yoktur. Bu durumlar arasındaki temel fark, yerçekimi kuvveti, mesafe ve parçacıklar arasındaki hareket özgürlüğüdür. Madde ısı alışverişi yaparak bir durumdan diğerine geçebilir."),

 dict(text_id="T036", label="humanized", prompt_id=2, model="Claude", humanizer="Aithor", source_text_id="T034",
  raw_text="Madde, doğada katı, sıvı ve gaz hâlinde bulunur. Katı hâlde tanecikler birbirine çok yakındır ve düzenli bir biçimde titreşir. Bu nedenle katıların şekli ve hacmi bellidir. Örneğin buzdolabındaki buz küpü veya masamızın üzerindeki tahta kalem birer katıdır. Sıvı hâlde ise tanecikler arasındaki boşluk biraz artar ve tanecikler birbiri üzerinden kayabilir. Bu yüzden sıvılar bulundukları kabın şeklini alır ama hacimleri değişmez. Bardağa doldurduğumuz su bunun güzel bir örneğidir. Gaz hâlinde ise tanecikler çok uzak ve serbesttir; her yöne dağılırlar. Bu nedenle gazların şekli yoktur; ayrıca hacimleri de yoktur. Mutfak tüpündeki doğal gaz veya soluduğumuz hava buna örnektir. Bu hâller arasındaki en önemli fark, tanecikler arasındaki çekim kuvveti, uzaklık ve hareket serbestliğidir. Isı alışverişiyle madde bir hâlden diğerine geçebilir."),

 dict(text_id="T037", label="ai", prompt_id=3, model="Claude", humanizer="", source_text_id="",
  raw_text="Teknoloji, eğitimi hem kolaylaştıran hem de bazı yeni sorunlar doğuran güçlü bir araçtır. Olumlu yanı düşünüldüğünde, internet sayesinde bilgiye ulaşmak çok hızlanmış, uzaktan eğitim uygulamaları sayesinde farklı şehirlerde yaşayan öğrenciler aynı derse katılabilir hale gelmiştir. Görsel ve işitsel materyaller soyut konuları somutlaştırdığı için öğrenmeyi kalıcı kılar; öğrenciler kendi hızlarında ilerleme fırsatı bulur. Tekrar izlenebilen ders videoları, geride kalan öğrenciler için önemli bir destek sağlar. Ancak madalyonun diğer yüzünde ciddi riskler vardır. Sürekli ekran karşısında kalmak dikkat süresini kısaltmakta, öğrencileri hazır bilgiye alıştırarak araştırma ve düşünme çabasını azaltmaktadır. Ayrıca her ailenin aynı imkânlara sahip olmaması fırsat eşitsizliğini derinleştirir. Bana göre teknoloji tek başına ne iyi ne kötüdür; belirleyici olan, öğretmenin rehberliğinde bilinçli ve ölçülü kullanılmasıdır."),

 dict(text_id="T038", label="humanized", prompt_id=3, model="Claude", humanizer="Aithor", source_text_id="T037",
  raw_text="Teknoloji, eğitimi kolaylaştıran ve bazı yeni sorunlar getiren bir araçtır. Olumlu yanına bakarsak, internet sayesinde bilgiye ulaşmak çok daha hızlı hale gelmiştir. Uzaktan eğitim uygulamaları ile farklı şehirlerde yaşayan öğrenciler aynı derse katılabilmektedir. Görsel ve işitsel materyaller soyut konuları somutlaştırarak öğrenmeyi kalıcı hale getirir; öğrenciler kendi hızlarında ilerleme fırsatı bulurlar. Tekrar izlenebilen ders videoları geride kalan öğrencilere büyük destek sağlar. Ama diğer yüzünde ciddi riskler vardır. Sürekli ekran karşısında kalmak dikkat süresini kısaltır, öğrencileri hazır bilgiye alıştırarak araştırma ve düşünme çabasını azaltır. Her ailenin aynı imkânlara sahip olmaması fırsat eşitsizliğini derinleştirir. Bana göre teknoloji tek başına ne iyi ne kötü; belirleyici olan öğretmenin rehberliğinde bilinçli ve ölçülü kullanılmasıdır."),

 dict(text_id="T039", label="humanized", prompt_id=3, model="Claude", humanizer="Rephraser", source_text_id="T037",
  raw_text="Teknoloji eğitime yardımcı olan ama aynı zamanda bazı yeni sorunlar da yaratan güçlü bir araçtır. Olumlu tarafı, internet bilgiye erişimi çok daha hızlı hale getirdi ve uzaktan eğitim araçları artık farklı şehirlerdeki öğrencilerin aynı kurslara katılmasına olanak tanıyor. Görsel ve işitsel materyaller, öğrencilerin soyut kavramları somut hale getirerek bilgiyi akılda tutmalarına yardımcı olurken aynı zamanda kendi hızlarında öğrenmelerine de olanak sağlar. Tekrar izlenebilecek ders videoları, yetişmekte zorlanan öğrencilere çok önemli yardımlar sunuyor. Ancak madalyonun diğer tarafında önemli riskler var. Sürekli ekranlara bakmak, öğrencileri hazır bilgilere alıştırarak dikkat sürelerini kısaltır, araştırma ve düşünme çabalarını azaltır. Ayrıca tüm ailelerin eşit fırsatlara sahip olmadığı gerçeği, fırsat eşitsizliğini daha da artırmaktadır. Bana göre teknoloji kendi başına ne iyi ne de kötüdür; asıl önemli olan bunun bir öğretmen rehberliğinde bilinçli ve ölçülü uygulanmasıdır."),

 dict(text_id="T040", label="ai", prompt_id=4, model="Claude", humanizer="", source_text_id="",
  raw_text="Etkili bir sınav hazırlığı, öncelikle sınavın kapsamını ve tarihini net biçimde öğrenmekle başlar; öğrenci hangi konulardan sorumlu olduğunu bilmeden plan yapamaz. İkinci adımda kalan süreyi konulara bölen, günlük ve haftalık hedefler içeren gerçekçi bir çalışma programı hazırlanmalıdır. Ardından öğrenci ders notlarını, kitapları ve öğretmenin verdiği kaynakları toplayarak konuları anlayarak okumalı, önemli noktaları kendi cümleleriyle özetlemelidir. Öğrenmenin kalıcı olması için bol soru çözmek, çıkmış sınavları denemek ve yanlışları not alarak eksik kalan konulara geri dönmek gerekir. Çalışma sırasında düzenli aralar vermek, uyku ve beslenmeye dikkat etmek de başarıyı doğrudan etkiler. Son adımda ise öğrenci sınavdan bir ya da iki gün önce yeni konu öğrenmek yerine tekrar yapmalı ve sınava dinlenmiş, sakin bir zihinle girmelidir."),

 dict(text_id="T041", label="humanized", prompt_id=4, model="Claude", humanizer="Aithor", source_text_id="T040",
  raw_text="Etkili bir sınav hazırlığı, öncelikle sınavın kapsamını ve tarihini net biçimde öğrenmekle başlar; öğrenci hangi konulardan sorumlu olduğunu bilmeden plan yapamaz. İkinci adımda kalan süreyi konulara bölen, günlük ve haftalık hedefler içeren gerçekçi bir çalışma programı hazırlanmalıdır. Ardından öğrenci ders notlarını, kitapları ve öğretmenin verdiği kaynakları toplayarak konuları anlayarak okumalı, önemli noktaları kendi cümleleriyle özetlemelidir. Öğrenmenin kalıcı olması için bol soru çözmek, çıkmış sınavları denemek ve yanlışları not alarak eksik kalan konulara geri dönmek gerekir. Çalışma sırasında düzenli aralar vermek, uyku ve beslenmeye dikkat etmek de başarıyı doğrudan etkiler. Son adımda ise öğrenci sınavdan bir ya da iki gün önce yeni konu öğrenmek yerine tekrar yapmalı ve sınava dinlenmiş, sakin bir zihinle girmelidir."),

 dict(text_id="T042", label="humanized", prompt_id=4, model="Claude", humanizer="Rephraser", source_text_id="T040",
  raw_text="Etkili sınav hazırlığı sınavın kapsamını ve tarihini net bir şekilde anlamakla başlar, çünkü öğrenci hangi konulardan sorumlu olduğunu bilmeden plan oluşturamaz. İkinci adımda kalan zamanı belirli konulara ayıran, günlük ve haftalık hedefler koyan gerçekçi bir çalışma planı oluşturmalısınız. Daha sonra öğrenci, öğretmenin sağladığı ders notlarını, kitapları ve kaynakları toplamalı, konuları dikkatlice okuyarak anlayacak ve önemli noktaları kendi cümleleriyle özetlemelidir. Bağlı kalmayı öğrenmek için birçok soruyu yanıtlamalı, deneme sınavlarına girmeli, hatalarınızı kaydetmeli ve kaçırdığınız konuları gözden geçirmelisiniz. Düzenli molalar vermek, yeterince uyumak ve iyi beslenmek de başarınızı doğrudan etkiler. Son adımda öğrenci sınavdan bir veya iki gün önce yeni bir konu öğrenmek yerine materyali gözden geçirip ardından dinlenmiş ve sakin bir zihinle sınava girmelidir."),

 dict(text_id="T043", label="ai", prompt_id=5, model="Claude", humanizer="", source_text_id="",
  raw_text="Yüz yüze eğitim, öğretmen ve öğrencinin aynı ortamda bulunmasına dayandığı için iletişimi güçlendirir; beden dili, anlık geri bildirim ve sınıf içi etkileşim öğrenmeyi kolaylaştırır. Ayrıca laboratuvar, atölye gibi uygulamalı çalışmalar bu modelde daha verimlidir. Öğrenciler arasında kurulan arkadaşlık bağları da kişisel gelişimi destekler. Buna karşılık ulaşım masrafı, zaman kaybı ve sabit ders saatleri önemli sınırlılıklar olarak öne çıkar. Uzaktan eğitim ise mekândan bağımsız olması, kayıtlı derslerin tekrar izlenebilmesi ve öğrencinin kendi hızında ilerleyebilmesi sayesinde esneklik sunar; maliyeti de genellikle daha düşüktür. Ancak internet ve cihaz erişimindeki eşitsizlikler, dikkat dağınıklığı, sosyalleşme eksikliği ve öz disiplin gerekliliği başlıca dezavantajlarıdır. Sonuç olarak iki yöntem birbirinin rakibi değil tamamlayıcısıdır; harmanlanmış modeller her iki yaklaşımın güçlü yönlerini bir araya getirebilir."),

 dict(text_id="T044", label="humanized", prompt_id=5, model="Claude", humanizer="Aithor", source_text_id="T043",
  raw_text="Yüz yüze eğitim, öğretmen ve öğrencinin aynı ortamda bulunmasına dayandığı için iletişimi güçlendirir; beden dili, anlık geri bildirim ve sınıf içi etkileşim öğrenmeyi kolaylaştırır. Ayrıca laboratuvar, atölye gibi uygulamalı çalışmalar bu modelde daha verimlidir. Öğrenciler arasında kurulan arkadaşlık bağları da kişisel gelişimi destekler. Buna karşılık ulaşım masrafı, zaman kaybı ve sabit ders saatleri önemli sınırlılıklar olarak öne çıkar. Uzaktan eğitim ise mekândan bağımsız olması, kayıtlı derslerin tekrar izlenebilmesi ve öğrencinin kendi hızında ilerleyebilmesi sayesinde esneklik sunar; maliyeti de genellikle daha düşüktür. Ancak internet ve cihaz erişimindeki eşitsizlikler, dikkat dağınıklığı, sosyalleşme eksikliği ve öz disiplin gerekliliği başlıca dezavantajlarıdır. Sonuç olarak iki yöntem birbirinin rakibi değil tamamlayıcısıdır; harmanlanmış modeller her iki yaklaşımın güçlü yönlerini bir araya getirebilir."),

 dict(text_id="T045", label="humanized", prompt_id=5, model="Claude", humanizer="Rephraser", source_text_id="T043",
  raw_text="Yüz yüze eğitim iletişimi güçlendirir çünkü öğretmen ve öğrenci aynı ortamı paylaşır; burada beden dili, anında geri bildirim ve sınıf içi etkileşim öğrenmeyi kolaylaştırmaya yardımcı olur. Ayrıca laboratuvar, atölye gibi uygulamalı çalışmalar bu modelde daha verimlidir. Öğrencilerin kurdukları arkadaşlıklar aynı zamanda onların birey olarak gelişmelerine de yardımcı olur. Bunun tersine, ulaşım masrafları, kaybedilen zaman ve sabit ders süreleri önemli kısıtlar olarak ortaya çıkmaktadır. Öte yandan uzaktan eğitim, konumdan bağımsız olması, kayıtlı dersleri yeniden izleme olanağı ve kendi hızınızda öğrenme seçeneği nedeniyle esneklik sağlar ve bunların hepsi genellikle daha az maliyetlidir. Ancak ana dezavantajları arasında internete ve cihazlara eşit olmayan erişim, dikkat dağıtıcı unsurlar, sosyal etkileşimin azalması ve öz disiplin gerekliliği yer alıyor. Sonuç olarak, iki yöntem birbiriyle rekabet etmek yerine birbirini tamamlayarak harmanlanmış modellerin her iki yaklaşımın güçlü yanlarından yararlanmasına olanak tanır."),

 dict(text_id="T046", label="ai", prompt_id=1, model="Kumru", humanizer="", source_text_id="",
  raw_text="Türkiye Cumhuriyeti, 29 Ekim 1923'te Mustafa Kemal Atatürk liderliğinde ilan edilen bir cumhuriyettir. Başkenti Ankara'dır. Yönetim biçimi cumhuriyet olan Türkiye, laiklik ve eşitlik ilkelerine dayanır. Ülke; yasama (TBMM), yürütme (Cumhurbaşkanı ve hükümet) ve yargı erkleriyle yönetilir. Yargı bağımsızlığı anayasayla güvence altına alınmıştır. Cumhuriyet yönetiminde halk seçimlerle temsilcilerini seçer ve bu temsilciler ülkeyi yönetir. Yasama yetkisi TBMM'ye; yürütme yetkisi ise Cumhurbaşkanı ve onun belirlediği bakanlar kuruluna aittir. Yönetim biçiminde demokrasi, insan hakları ve hukukun üstünlüğü temel ilkelerdir ve devletin tüm kurumları bu ilkeler çerçevesinde işler. Türkiye, köklü bir tarihe ve zengin bir kültürel mirasa sahiptir; aynı zamanda çağdaşlaşma yolunda önemli adımlar atmaktadır."),

 dict(text_id="T047", label="ai", prompt_id=2, model="Kumru", humanizer="", source_text_id="",
  raw_text="Maddenin üç temel hâli vardır: katı, sıvı ve gaz. Katı hâl; maddenin belirli bir şekle sahip olduğu, genellikle dışarıdan bir etki olmadan şeklini koruduğu durumdur. Örneğin; buz veya kurşun kalem gibi maddeler bu hâle sahiptir. Sıvı hâl ise; maddenin akışkanlık gösterdiği ve bulunduğu kabın şeklini aldığı durumdur. Su ya da süt gibi (sıvı yağ gibi) maddeler bu hâli yaşar. Gaz hâli; maddenin en düzensiz hâlidir ve bulunduğu kabı tamamen doldurur ya da taşarak hacmini artırır. Hava (balon içindeki hava) veya helyum gazı (hava gazı gibi) bu duruma örnektir. Bu üç hâl maddeyi birbirinden ayıran en temel özelliklerdir ve hepsi de maddenin farklı hallerini temsil eder."),

 dict(text_id="T048", label="humanized", prompt_id=1, model="Kumru", humanizer="Aithor", source_text_id="T046",
  raw_text="Türkiye Cumhuriyeti, 29 Ekim 1923'te Mustafa Kemal Atatürk tarafından ilan edilen bir cumhuriyettir. Başkenti Ankara'dır. Türkiye, yönetim biçimi olarak cumhuriyet benimsemiş bir devlettir ve laiklik ile eşitlik ilkelerine bağlıdır. Ülke yasama (Türkiye Büyük Millet Meclisi), yürütme (Cumhurbaşkanı ve hükümet) ve yargı erkleriyle yönetilmektedir. Yargı bağımsızlığı anayasayla güvence altına alınmıştır. Cumhuriyet yönetiminde halk seçimlerle temsilcilerini seçer ve bu temsilciler ülkeyi yönetir. Yasama yetkisi Türkiye Büyük Millet Meclisi'ne; yürütme yetkisi ise Cumhurbaşkanı ve onun belirlediği bakanlar kuruluna aittir. Yönetim biçiminde demokrasi, insan hakları ve hukukun üstünlüğü temel ilkelerdir; devletin tüm kurumları bu ilkeler çerçevesinde işler. Türkiye, köklü bir tarihe sahip zengin kültürel mirasa sahiptir; aynı zamanda çağdaşlaşma yolunda önemli adımlar atmaktadır."),

 dict(text_id="T049", label="humanized", prompt_id=1, model="Kumru", humanizer="Rephraser", source_text_id="T046",
  raw_text="Türkiye Cumhuriyeti, 29 Ekim 1923'te Mustafa Kemal Atatürk'ün önderliğinde cumhuriyet olarak kuruldu. Başkenti Ankara'dır. Türkiye, laiklik ve eşitlik ilkeleri üzerine kurulmuş bir cumhuriyettir. Ülke; Yasama (Türkiye Büyük Millet Meclisi), yürütme (Cumhurbaşkanlığı ve hükümet) ve yargı organları tarafından yönetilir. Anayasa yargı bağımsızlığını güvence altına alıyor. Cumhuriyette halk, temsilcilerini seçimlerle seçer ve bu temsilciler ülkeyi yönetir. Yasama yetkisi Türkiye Büyük Millet Meclisi'nde, yürütme yetkisi ise Cumhurbaşkanı ve onun atadığı Bakanlar Kurulu'ndadır. Demokrasi, insan hakları ve hukukun üstünlüğü, hükümetin temel ilkeleri olarak hizmet etmekte ve tüm devlet kurumlarının bu yerleşik çerçeve içerisinde işlemesini sağlamaktadır. Türkiye köklü bir tarihe ve zengin bir kültürel mirasa sahip olmakla birlikte aynı zamanda modernleşme yolunda da önemli adımlar atmaktadır."),

 dict(text_id="T050", label="humanized", prompt_id=2, model="Kumru", humanizer="Aithor", source_text_id="T047",
  raw_text="Maddenin üç temel hali vardır: katı, sıvı ve gaz. Katı hâl, maddenin belirli bir şekle sahip olduğu ve genellikle dışarıdan bir etki olmadan şeklini koruduğu durumdur. Örneğin; buz veya kurşun kalem gibi maddeler bu hâle sahiptir. Sıvı hâl ise; maddenin akışkanlık gösterdiği ve bulunduğu kabın şeklini aldığı durumdur. Su ya da süt gibi (sıvı yağ gibi) maddeler bu hâli yaşar. Gaz hâli; maddenin en düzensiz hâlidir ve bulunduğu kabı tamamen doldurur ya da taşarak hacmini artırır. Hava (balon içindeki hava) veya helyum gazı (hava gazı gibi) bu duruma örnektir. Bu üç hal maddeyi birbirinden ayıran en temel özelliklerdir ve hepsi de maddenin farklı hallerini temsil eder."),

 dict(text_id="T051", label="humanized", prompt_id=2, model="Kumru", humanizer="Rephraser", source_text_id="T047",
  raw_text="Madde üç temel halde bulunur: katı, sıvı ve gaz. Katı hal; bu, bir maddenin belirli bir şekle sahip olduğu ve genellikle herhangi bir dış kuvvet olmaksızın bu şekli koruduğu bir durumdur. Örneğin buz, kalem gibi maddeler bu durumdadır. Sıvı hal, bir maddenin aktığı ve bulunduğu kabın şekline uyduğu durum olarak tanımlanır. Su veya süt gibi maddeler (örneğin yağ) bu durumdan geçer. Gaz halindeki madde en düzensiz halindedir ve ya bulunduğu kabı tamamen dolduracak ya da taşarak genişleyecektir. Hava (balonun içindeki hava) veya helyum gazı (örneğin, genellikle \"hava gazı\" olarak adlandırılan gaz) bu senaryonun örnekleridir. Bu üç durum, maddenin bir biçimini diğerinden ayıran temel özelliklerdir ve her biri maddenin ayrı bir durumunu temsil eder."),

 dict(text_id="T052", label="ai", prompt_id=3, model="Kumru", humanizer="", source_text_id="",
  raw_text="Teknoloji, eğitimde hem fırsatları hem de bazı zorlukları beraberinde getirmiştir. Olumlu bir açıdan, teknoloji sayesinde bilgiye erişim kolaylaşmıştır; örneğin çevrimiçi dersler sayesinde dünyanın farklı noktalarındaki öğrencilere eğitim olanakları sunulabilmektedir. Ayrıca, teknolojik araçlar sayesinde eğitimde bireyselleştirme ve erişilebilirlik artmıştır. Olumsuz açıdan bakıldığındaysa, bazı öğrenciler bu teknolojik imkânlardan yeterince faydalanamamakta ve dijital uçurum dediğimiz bir eşitsizlik ortaya çıkabilmektedir. Özellikle kırsal bölgelerde veya teknolojiye erişimi kısıtlı olan öğrenciler, klasik yöntemlerle eğitim almakta; bu da öğrenme süreçlerini sekteye uğratabilmektedir. Sonuç olarak, teknolojinin eğitimdeki olumlu etkileri kadar olumsuz etkileri de bulunmaktadır ve her iki durum da dengeli bir şekilde ele alınmalıdır. Eğitim politikalarının bu etkileri dikkate alarak düzenlenmesi büyük önem taşır."),

 dict(text_id="T053", label="humanized", prompt_id=3, model="Kumru", humanizer="Aithor", source_text_id="T052",
  raw_text="Teknoloji eğitimde fırsatlar ve zorluklar getirmiştir. İyi bir yönü, teknoloji ile bilgiye ulaşmak kolaylaşmıştır; örneğin online dersler ile dünyanın farklı yerlerindeki öğrencilere eğitim imkânları sunulabilmektedir. Ayrıca, teknolojik araçlar ile eğitimde kişiye özel olma ve ulaşılabilirlik artmıştır. Kötü bir yönü ise bazı öğrenciler bu teknolojik imkânlardan yeterince yararlanamayarak dijital uçurum dediğimiz bir eşitsizlik ortaya çıkabilmektedir. Özellikle kırsal alanlarda ya da teknolojiye erişimi kısıtlı olan öğrenciler klasik yöntemlerle eğitim almakta bu da öğrenme süreçlerini aksatabilmektedir. Sonuç olarak, teknolojinin eğitimdeki iyi etkileri kadar kötü etkileri de vardır ve her iki durum dengeli bir şekilde ele alınmalıdır. Eğitim politikalarının bu etkileri dikkate alarak düzenlenmesi çok önemlidir."),

 dict(text_id="T054", label="humanized", prompt_id=3, model="Kumru", humanizer="Rephraser", source_text_id="T052",
  raw_text="Teknoloji eğitim için hem fırsatlar hem de bazı zorluklar yarattı. İşin iyi tarafı, teknoloji bilgiye erişimi kolaylaştırdı; örneğin, çevrimiçi kurslar artık dünyanın her yerinden öğrencilerin eğitime erişmesine olanak tanıyor. Ayrıca teknolojik araçlar eğitimde bireyselleşmeyi ve erişilebilirliği artırmıştır. İşin olumsuz tarafı ise bazı öğrencilerin bu teknolojik fırsatlardan tam anlamıyla yararlanamaması olabilir ve bu da potansiyel olarak dijital uçurum olarak bilinen bir boşluğa yol açabilir. Kırsal bölgelerdeki veya sınırlı teknoloji erişimine sahip öğrenciler genellikle geleneksel öğretim yöntemlerine güveniyor ve bu da öğrenmelerini aksatabiliyor. Sonuç olarak eğitimde teknolojinin hem yararları hem de sakıncaları vardır ve her iki boyutun da dengeli bir şekilde yönetilmesi gerekmektedir. Eğitim politikalarının bu etkileri dikkate alarak tasarlanması büyük önem taşımaktadır."),

 dict(text_id="T055", label="ai", prompt_id=4, model="Kumru", humanizer="", source_text_id="",
  raw_text="Bir öğrencinin sınava etkili şekilde hazırlanması için öncelikle hedefini belirlemesi önemlidir. Ardından, günlük çalışma programı oluşturmalıdır. Her gün belirli saatlerde, konu tekrarı yaparak ve test çözerek eksiklerini gidermelidir. Zorlandığı konuları not almalı; gerekirse öğretmenlerinden veya arkadaşlarından yardım istemelidir. Düzenli tekrar alışkanlığı kazanmak, bilgilerin kalıcı olmasını sağlar. Uyku düzenine dikkat etmeli; yeterli uyumaya özen göstermelidir. Beslenmesine dikkat etmeli ve sağlıklı beslenmeye özen göstermelidir. Stresten uzak durmak için nefes egzersizleri veya kısa yürüyüşler yapabilir. Başarıya ulaşmak için zaman yönetimi de çok önemlidir: Her dersten sonra kısa molalar vererek dinlenmeli ve ardından bir sonraki derse odaklanmalıdır. Son olarak, sınav öncesi deneme sınavları çözmek; eksiklerini görmek ve sınav stresini yönetmek açısından faydalıdır."),

 dict(text_id="T056", label="humanized", prompt_id=4, model="Kumru", humanizer="Aithor", source_text_id="T055",
  raw_text="Bir öğrencinin sınava iyi hazırlanması için önce hedefini belirlemesi gerekir. Sonra, günlük çalışma programı yapmalıdır. Her gün belli saatlerde, konu tekrarı yaparak ve test çözerek eksiklerini kapatmalıdır. Zorlandığı konuları not almalı; gerekirse öğretmenlerinden veya arkadaşlarından yardım istemelidir. Düzenli tekrar alışkanlığı kazanmak, bilgilerin kalıcı olmasını sağlar. Uyku düzenine dikkat etmeli; yeterli uyumaya özen göstermelidir. Beslenmesine dikkat etmeli ve sağlıklı beslenmeye özen göstermelidir. Stresten uzak durmak için nefes egzersizleri veya kısa yürüyüşler yapabilir. Başarıya ulaşmak için zaman yönetimi de çok önemlidir: Her dersten sonra kısa molalar vererek dinlenmeli ve ardından bir sonraki derse odaklanmalıdır. Son olarak, sınav öncesi deneme sınavları çözmek; eksiklerini görmek ve sınav stresini yönetmek açısından faydalıdır."),

 dict(text_id="T057", label="humanized", prompt_id=4, model="Kumru", humanizer="Rephraser", source_text_id="T055",
  raw_text="Sınava etkili bir şekilde hazırlanabilmek için öğrencinin öncelikle hedefini belirlemesi gerekir. Daha sonra günlük bir çalışma programı oluşturmalısınız. Konuyu tekrar gözden geçirerek ve her gün belirli saatlerde testler yaparak zayıf yönlerini düzeltmelidir. Zorlayıcı konuları takip etmeli ve gerekirse öğretmenlerinden veya arkadaşlarından yardım almalıdır. Düzenli gözden geçirme alışkanlığını geliştirmek, bilgilerin hafızanızda kalıcı olarak kalmasını sağlar. Yeterince dinlenmenizi sağlamak önemli olduğundan uyku programınıza odaklanmalısınız. Beslenmesine dikkat etmeli ve sağlıklı beslenmeye dikkat etmelidir. Nefes egzersizleri yaparak veya kısa yürüyüşler yaparak stresten uzak durabilir. Zaman yönetimi de başarı için çok önemlidir: Her dersten sonra, bir sonraki derse odaklanmadan önce kısa bir dinlenme molası verin. Son olarak, gerçek sınavdan önce deneme sınavlarına girin; bu, zayıf noktalarınızı belirlemenize ve sınav stresini yönetmenize yardımcı olur."),

 dict(text_id="T058", label="ai", prompt_id=5, model="Kumru", humanizer="", source_text_id="",
  raw_text="Yüz yüze eğitim, öğrencilerin öğretmenle ve arkadaşlarıyla aynı ortamda bulunmasını sağlayarak etkileşimi artırır. Bu tür bir eğitimde, öğrenciler ders materyallerine anında erişim sağlar ve grup çalışmaları sayesinde sosyal öğrenme fırsatları artar. Ancak, yüz yüze eğitimde dikkat dağınıklığı ve disiplin sorunları daha sık yaşanabilir; sınıf ortamında gürültü ve motivasyon kaybı gibi olumsuzluklar da gözlemlenebilir. Uzaktan eğitim ise bilgiye her yerden ve her zaman ulaşma imkanı sunar; öğrenciler kendi hızlarında çalışabilir ve kaynaklara diledikleri zaman erişebilirler. Ancak yüz yüze iletişimin eksikliği nedeniyle öğrencilerin motivasyonu düşebilir ve arkadaşlık ilişkileri zayıflayabilir. Ayrıca, teknik sorunlar ve internet bağlantısı problemleri, uzaktan eğitimin verimliliğini olumsuz etkileyebilir. Sonuç olarak; her iki yöntemin de farklı avantajları ve dezavantajları bulunmakta, öğrenci ihtiyaçlarına ve koşullara göre en uygun model seçilmelidir."),

 dict(text_id="T059", label="humanized", prompt_id=5, model="Kumru", humanizer="Aithor", source_text_id="T058",
  raw_text="Yüz yüze eğitim, öğrencilerin öğretmenle ve arkadaşlarıyla aynı ortamda bulunmasını sağlayarak etkileşimi artırır. Bu tür bir eğitimde, öğrenciler ders materyallerine anında erişim sağlar ve grup çalışmaları sayesinde sosyal öğrenme fırsatları artar. Ancak, yüz yüze eğitimde dikkat dağınıklığı ve disiplin sorunları daha sık yaşanabilir; sınıf ortamında gürültü ve motivasyon kaybı gibi olumsuzluklar da gözlemlenebilir. Uzaktan eğitim ise bilgiye her yerden ve her zaman ulaşma imkanı sunar; öğrenciler kendi hızlarında çalışabilir ve kaynaklara diledikleri zaman erişebilirler. Ancak yüz yüze iletişimin eksikliği nedeniyle öğrencilerin motivasyonu düşebilir ve arkadaşlık ilişkileri zayıflayabilir. Ayrıca teknik sorunlar ve internet bağlantısı problemleri uzaktan eğitimin verimliliğini olumsuz etkileyebilir. Sonuç olarak; her iki yöntemin de farklı avantajları ile dezavantajları var, öğrenci ihtiyaçlarına uygun en iyi model seçilmelidir."),

 dict(text_id="T060", label="humanized", prompt_id=5, model="Kumru", humanizer="Rephraser", source_text_id="T058",
  raw_text="Yüz yüze eğitim, öğrencilerin öğretmenleri ve akranlarıyla aynı alanı paylaşmasına olanak tanıyarak etkileşimi artırır. Bu eğitim türünde öğrenciler ders materyallerine anında ulaşabilmekte ve grup çalışmaları sayesinde sosyal öğrenme fırsatları artmaktadır. Ancak yüz yüze derslerde dikkat dağınıklığı ve disiplin sorunları daha sık yaşanabiliyor, gürültü, motivasyon düşüklüğü gibi sorunlar da görülebiliyor. Öte yandan uzaktan eğitim, bilgiye her yerden ve her zaman erişme şansını sunarak öğrencilerin kendi hızlarında çalışmalarına ve kaynakları ihtiyaç duydukları anda kullanmalarına olanak tanır. Ancak yüz yüze etkileşim olmazsa öğrencilerin motivasyonu düşebilir ve arkadaşlıkları zayıflayabilir. Ayrıca teknik aksaklıklar ve internet bağlantısı sorunları uzaktan eğitimin başarısını engelleyebilir. Sonuç olarak, her iki yöntemin de kendine göre artıları ve eksileri vardır, dolayısıyla öğrencilerin özel ihtiyaçlarına ve koşullarına göre en iyi model seçilmelidir."),
]

def s(tid, det, sc, bl, conf, ver, mode, kisa="hayir", tarih="2026-08-06", mixed=None):
    # mixed: GPTZero uc sinifli cikti verdiginde "Mixed" yuzdesi.
    # Skor her zaman AI yuzdesidir; Mixed bilgisi ayrica saklanir (duyarlilik analizi icin).
    return dict(text_id=tid, detector_name=det, detector_version=ver, scan_mode=mode,
                score=sc, binary_label=bl, threshold=0.50, confidence=conf,
                mixed_pct=mixed, kisa_metin_uyarisi=kisa, run_date=tarih)

G = ("GPTZero", "Model 4.1m", "Advanced")
Z = ("ZeroGPT", "web arayuz", "Detect Text")

SKORLAR = [
 s("T001",G[0],0.70,1,"moderately confident",G[1],G[2],tarih="2026-08-05"),
 s("T001",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-05"),
 s("T002",G[0],0.83,1,"highly confident",G[1],G[2],tarih="2026-08-05"),
 s("T002",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-05"),
 s("T003",G[0],0.12,0,"highly confident",G[1],G[2],kisa="EVET",tarih="2026-08-05"),
 s("T003",Z[0],0.308,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-05"),
 s("T004",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-05"),
 s("T004",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-05"),
 s("T005",G[0],0.19,0,"moderately confident",G[1],G[2],tarih="2026-08-05"),
 s("T005",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-05"),
 s("T006",G[0],0.61,1,"moderately confident",G[1],G[2],tarih="2026-08-05"),
 s("T006",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-05"),
 s("T007",G[0],0.99,1,"highly confident",G[1],G[2]),
 s("T007",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2]),
 s("T008",G[0],1.00,1,"highly confident",G[1],G[2]),
 s("T008",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2]),
 s("T009",G[0],0.77,1,"moderately confident",G[1],G[2]),
 s("T009",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2]),
 s("T010",G[0],1.00,1,"highly confident",G[1],G[2]),
 s("T010",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2]),
 s("T011",G[0],1.00,1,"highly confident",G[1],G[2]),
 s("T011",Z[0],0.241,0,"Most Likely Human written",Z[1],Z[2]),
 s("T012",G[0],0.47,0,"uncertain",G[1],G[2]),
 s("T012",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2]),
 s("T013",G[0],0.84,1,"highly confident",G[1],G[2]),
 s("T013",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2]),
 s("T014",G[0],0.39,0,"uncertain",G[1],G[2]),
 s("T014",Z[0],0.157,0,"Human written",Z[1],Z[2]),
 s("T015",G[0],0.03,0,"highly confident",G[1],G[2]),
 s("T015",Z[0],0.884,1,"AI/GPT Generated",Z[1],Z[2]),

 s("T016",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T016",Z[0],0.270,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T017",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T017",Z[0],0.270,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T018",G[0],0.96,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T018",Z[0],0.279,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T019",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T019",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T020",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T020",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T021",G[0],0.92,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T021",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T022",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T022",Z[0],0.399,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T023",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T023",Z[0],0.237,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T024",G[0],0.97,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T024",Z[0],0.7385,1,"mixed signals",Z[1],Z[2],tarih="2026-08-07"),
 s("T025",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T025",Z[0],0.555,1,"Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T026",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T026",Z[0],0.533,1,"Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T027",G[0],0.80,1,"moderately confident",G[1],G[2],tarih="2026-08-07"),
 s("T027",Z[0],0.2401,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T028",G[0],0.98,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T028",Z[0],0.390,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T029",G[0],0.89,1,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T029",Z[0],0.384,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-07"),
 s("T030",G[0],0.09,0,"highly confident",G[1],G[2],tarih="2026-08-07"),
 s("T030",Z[0],0.914,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-07"),
 s("T031",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-10"),
 s("T031",Z[0],0.875,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T032",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-10"),
 s("T032",Z[0],0.875,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T033",G[0],0.87,1,"highly confident",G[1],G[2],tarih="2026-08-10"),
 s("T033",Z[0],1.000,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T034",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-10"),
 s("T034",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T035",G[0],0.72,1,"moderately confident",G[1],G[2],tarih="2026-08-10"),
 s("T035",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T036",G[0],0.91,1,"highly confident",G[1],G[2],tarih="2026-08-10"),
 s("T036",Z[0],0.000,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T037",G[0],0.95,1,"highly confident",G[1],G[2],tarih="2026-08-10"),
 s("T037",Z[0],0.259,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T038",G[0],0.03,0,"highly confident - MIXED (6/9 cumle YZ)",G[1],G[2],tarih="2026-08-10",mixed=0.92),
 s("T038",Z[0],0.309,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T039",G[0],0.02,0,"highly confident - HUMAN",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T039",Z[0],0.755,1,"mixed signals",Z[1],Z[2],tarih="2026-08-10"),
 s("T040",G[0],0.98,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T040",Z[0],0.688,1,"mixed signals",Z[1],Z[2],tarih="2026-08-10"),
 s("T041",G[0],0.98,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T041",Z[0],0.688,1,"mixed signals",Z[1],Z[2],tarih="2026-08-10"),
 s("T042",G[0],0.59,1,"uncertain",G[1],G[2],tarih="2026-08-10",mixed=0.01),
 s("T042",Z[0],0.5817,1,"Likely Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T043",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T043",Z[0],0.328,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T044",G[0],1.00,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T044",Z[0],0.328,0,"Most Likely Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T045",G[0],0.05,0,"moderately confident (mix)",G[1],G[2],tarih="2026-08-10",mixed=0.74),
 s("T045",Z[0],0.602,1,"Likely Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T046",G[0],0.01,0,"highly confident (mix)",G[1],G[2],tarih="2026-08-10",mixed=0.95),
 s("T046",Z[0],0.881,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T047",G[0],0.58,1,"uncertain",G[1],G[2],tarih="2026-08-10",mixed=0.01),
 s("T047",Z[0],0.00,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T048",G[0],0.10,0,"moderately confident (mix)",G[1],G[2],tarih="2026-08-10",mixed=0.80),
 s("T048",Z[0],0.982,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T049",G[0],0.00,0,"highly confident human",G[1],G[2],tarih="2026-08-10",mixed=0.04),
 s("T049",Z[0],0.982,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T050",G[0],0.20,0,"moderately confident human",G[1],G[2],tarih="2026-08-10",mixed=0.01),
 s("T050",Z[0],0.00,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T051",G[0],0.21,0,"moderately confident human",G[1],G[2],tarih="2026-08-10",mixed=0.01),
 s("T051",Z[0],0.00,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T052",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T052",Z[0],1.00,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T053",G[0],0.78,1,"moderately confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T053",Z[0],1.00,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T054",G[0],0.97,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T054",Z[0],1.00,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T055",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T055",Z[0],0.131,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T056",G[0],0.96,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T056",Z[0],0.00,0,"Human written",Z[1],Z[2],tarih="2026-08-10"),
 s("T057",G[0],0.11,0,"highly confident human",G[1],G[2],tarih="2026-08-10",mixed=0.07),
 s("T057",Z[0],0.8475,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T058",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T058",Z[0],1.00,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T059",G[0],0.99,1,"highly confident",G[1],G[2],tarih="2026-08-10",mixed=0.00),
 s("T059",Z[0],1.00,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
 s("T060",G[0],0.68,1,"moderately confident",G[1],G[2],tarih="2026-08-10",mixed=0.01),
 s("T060",Z[0],1.00,1,"AI/GPT Generated",Z[1],Z[2],tarih="2026-08-10"),
]

# ----------------------------------------------------------------------
texts = pd.DataFrame(METINLER)
texts["word_count"] = texts["raw_text"].str.split().str.len()
texts["char_count"] = texts["raw_text"].str.len()
texts["ai_uzunluk_bandi"] = texts.apply(
    lambda r: "uygulanmaz" if r["label"] != "ai"
    else ("uygun" if 100 <= r["word_count"] <= 120 else "bant disi"), axis=1)

# Kelime ortusme orani: insanlastirilmis metnin kaynak metinle ortak kelime yuzdesi.
# Donusum gucunun vekil olcusudur; %100 = arac metni hic degistirmemistir.
_kelime = {r["text_id"]: set(r["raw_text"].split()) for _, r in texts.iterrows()}
def _ortusme(r):
    src = r["source_text_id"]
    if r["label"] != "humanized" or not isinstance(src, str) or src not in _kelime:
        return None
    a = _kelime[src]
    return round(len(a & _kelime[r["text_id"]]) / len(a) * 100, 1) if a else None
texts["ortusme_orani"] = texts.apply(_ortusme, axis=1)
texts["degistirmedi"] = texts["ortusme_orani"].apply(
    lambda v: "evet" if v is not None and v >= 99.9 else ("hayir" if v is not None else ""))

scores = pd.DataFrame(SKORLAR)

os.makedirs("data_raw", exist_ok=True)
os.makedirs("results", exist_ok=True)
texts.to_csv("data_raw/texts.csv", index=False, encoding="utf-8-sig")
scores.to_csv("data_raw/detector_scores.csv", index=False, encoding="utf-8-sig")

print(texts.groupby(["model","label"]).size().to_string())
print()
print("Toplam metin:", len(texts), "| Toplam olcum:", len(scores))
print()

m = scores.merge(texts[["text_id","prompt_id","label","humanizer","model"]], on="text_id")
satirlar = []
for (mdl, pid), _ in m.groupby(["model","prompt_id"]):
    ai_ids = texts[(texts.model==mdl)&(texts.prompt_id==pid)&(texts.label=="ai")]["text_id"].tolist()
    if not ai_ids: continue
    ai_id = ai_ids[0]
    for d in sorted(m.detector_name.unique()):
        sub = m[(m.model==mdl)&(m.prompt_id==pid)&(m.detector_name==d)].set_index("text_id")
        if ai_id not in sub.index: continue
        base = float(sub.loc[ai_id,"score"])
        for tid in sub.index:
            if tid == ai_id: continue
            arac = texts.loc[texts.text_id==tid,"humanizer"].values[0]
            val = float(sub.loc[tid,"score"])
            satirlar.append(dict(model=mdl, prompt=pid, dedektor=d, arac=arac,
                                 ai=round(base,3), humanized=round(val,3),
                                 fark_puan=round((val-base)*100,1),
                                 aciklama="OLCULEMEZ - taban etkisi" if base<=0.0 else ""))
ev = pd.DataFrame(satirlar)
ev.to_csv("results/kacirma_ozet.csv", index=False, encoding="utf-8-sig")
print(ev.to_string(index=False))
print("\nKaydedildi -> data_raw/ ve results/")

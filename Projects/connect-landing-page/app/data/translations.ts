
export interface Translation {
  nav: { coverage: string; pricing: string; tech: string; api: string };
  hero: {
    b2c_tag: string; b2c_title_1: string; b2c_title_2: string; b2c_desc: string;
    b2c_btn_1: string; b2c_btn_2: string; b2b_tag: string; b2b_title_1: string;
    b2b_title_2: string; b2b_desc: string; b2b_btn_1: string; b2b_btn_2: string;
    loc_detecting: string; loc_found: string; support_whatsapp: string;
    search_placeholder: string; popular_dest: string;
    app_title: string; app_desc: string; app_ios: string; app_android: string;
    app_features: Array<{ title: string; desc: string }>;
  };
  testimonials: {
    title: string;
    items: Array<{ name: string; role: string; text: string }>;
  };
  calculator: {
    title: string; label: string; saving: string; per_year: string;
  };
  dashboard: {
    title: string; nodes: string; traffic: string; latency: string; status: string;
    israel_optimized: string;
  };
  startup_section: { title: string; desc: string; features: string[] };
  stats: { countries: string; speed: string; privacy: string; uptime: string };
  pricing: {
    b2c_title: string; b2c_subtitle: string; b2b_title: string; b2b_subtitle: string;
    plans: Record<string, { name: string; desc: string }>;
    units: Record<string, string>;
  };
  config: {
    title: string; gb: string; mins: string; sms: string; confirm: string; total: string;
  };
  checkout: {
    title: string; step_final: string; apple_pay: string; plan: string;
    config: string; total_due: string; pay_now: string; success: string;
    success_desc: string; close: string;
  };
  footer: string;
}

export const translations: Record<string, Translation> = {
  "en": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ru": {
    "nav": {
      "coverage": "Покрытие",
      "pricing": "Цены",
      "tech": "Технология",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Глобальный роуминг отменен",
      "b2c_title_1": "Мир Твой.",
      "b2c_title_2": "Просто подключись.",
      "b2c_desc": "Мгновенный доступ к eSIM интернету в 190+ странах. Предоплаченные пакеты трафика без скрытых комиссий.",
      "b2c_btn_1": "Найти страну",
      "b2c_btn_2": "Скачать Приложение",
      "b2b_tag": "Инфраструктура Трафика Класса Enterprise",
      "b2b_title_1": "Масштабируемая",
      "b2b_title_2": "Среда Связи.",
      "b2b_desc": "Премиум трафик для бизнеса. API интеграция, выделенные каналы, оптовые пакеты данных и управление тысячами подключений.",
      "b2b_btn_1": "Начать Интеграцию",
      "b2b_btn_2": "Связаться с Sales",
      "loc_detecting": "Определяем вашу локацию...",
      "loc_found": "Лучший план для России:",
      "support_whatsapp": "Поддержка в WhatsApp",
      "search_placeholder": "Куда вы летите?",
      "popular_dest": "Популярные направления",
      "app_title": "Приложение Connect.Global",
      "app_desc": "Управляйте своими eSIM, отслеживайте расход трафика в реальном времени и пополняйте баланс из любой точки мира.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Мгновенная активация",
          "desc": "Физическая SIM не нужна"
        },
        {
          "title": "Безопасные платежи",
          "desc": "Apple Pay и Крипта"
        },
        {
          "title": "Отслеживание данных",
          "desc": "Виджет для iOS/Android"
        },
        {
          "title": "Мульти-девайс",
          "desc": "До 5 активных eSIM"
        }
      ]
    },
    "testimonials": {
      "title": "Нам доверяют лидеры",
      "items": [
        {
          "name": "Ари Л.",
          "role": "CTO @ Fintech Startup",
          "text": "Интеграция через API прошла идеально. Управляем более чем 500 подключениями без сбоев."
        },
        {
          "name": "Сара М.",
          "role": "CEO @ E-commerce Agency",
          "text": "Наконец-то eSIM провайдер, который понимает масштабы бизнеса. Лучшие цены на трафик в EU/US."
        }
      ]
    },
    "calculator": {
      "title": "Калькулятор выгоды B2B",
      "label": "Месячный объем данных",
      "saving": "Вы экономите до",
      "per_year": "в год"
    },
    "dashboard": {
      "title": "Live Сетевая Активность",
      "nodes": "Активные узлы",
      "traffic": "Текущий трафик",
      "latency": "Задержка",
      "status": "Статус системы: Штатно",
      "israel_optimized": "Оптимизировано для IL сетей (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Для Hi-Tech & Стартапов",
      "desc": "Инфраструктура, которой доверяют в Тель-Авиве. Мгновенное масштабирование для скрапинга, маркетинга и удаленной работы.",
      "features": [
        "5G низкая задержка",
        "Безлимитный доступ к API",
        "Корпоративный биллинг"
      ]
    },
    "stats": {
      "countries": "Стран покрытия",
      "speed": "Максимальная скорость",
      "privacy": "Полная приватность",
      "uptime": "Uptime гарантия"
    },
    "pricing": {
      "b2c_title": "Пакеты для Путешествий",
      "b2c_subtitle": "Честные гигабайты на максимальной скорости. Неиспользованный трафик сгорает в конце срока, обеспечивая нам возможность держать лучшие цены.",
      "b2b_title": "Инфраструктурные Тарифы",
      "b2b_subtitle": "Оптовая закупка трафика. Подключайте своих пользователей через наш API. Вы платите за общий пул, ваши клиенты платят вам.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Идеально для карт и мессенджеров на короткую поездку."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Хватит на звонки, работу и соцсети на целый месяц."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Максимум свободы. Стриминг, видео 4K и раздача интернета."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "Для небольших команд и арбитраж-тестов."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "Для маркетинговых агентств с большим расходом."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Интеграция в ваше приложение (White Label)."
        }
      },
      "units": {
        "pack": "пакет",
        "month": "мес",
        "days": "дней",
        "instant": "Мгновенная активация (QR)",
        "hidden_fees": "Без скрытых списаний",
        "hotspot": "Разрешена раздача (Hotspot)",
        "traffic": "Трафика",
        "api_access": "API Ключ доступа",
        "pool_ip": "Выделенный пул IP",
        "pool_label": "TB Pool",
        "select": "Выбрать",
        "start": "Начать работу"
      }
    },
    "config": {
      "title": "Настройка тарифа",
      "gb": "Данные (ГБ)",
      "mins": "Звонки (Мин)",
      "sms": "Пакет SMS",
      "confirm": "Перейти к оплате",
      "total": "Итого в месяц"
    },
    "checkout": {
      "title": "Безопасная оплата",
      "step_final": "Финальный шаг",
      "apple_pay": "Apple Pay",
      "plan": "Тариф",
      "config": "Конфигурация",
      "total_due": "Итого к оплате",
      "pay_now": "Оплатить сейчас",
      "success": "Активация успешна!",
      "success_desc": "Ваша eSIM готова. Проверьте почту для получения QR-кода.",
      "close": "Закрыть"
    },
    "footer": "Connect.Global © 2026. Все системы работают штатно."
  },
  "he": {
    "nav": {
      "coverage": "כיסוי",
      "pricing": "מחירים",
      "tech": "טכנולוגיה",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "נדידה גלובלית בוטלה",
      "b2c_title_1": "העולם שלך.",
      "b2c_title_2": "פשוט להתחבר.",
      "b2c_desc": "גישה מיידית לאינטרנט eSIM ב-190+ מדינות. חבילות גלישה בתשלום מראש ללא עמלות נסתרות.",
      "b2c_btn_1": "מצא מדינה",
      "b2c_btn_2": "הורד את האפליקציה",
      "b2b_tag": "תשתית תעבורה ברמת Enterprise",
      "b2b_title_1": "סביבת",
      "b2b_title_2": "קישוריות ניתנת להרחבה.",
      "b2b_desc": "תעבורה פриמיום לעסקים. אינטגרציה של API, ערוצים ייעודיים, חבילות נתונים בסיטונאות וניהול אלפי חיבורים.",
      "b2b_btn_1": "התחל אינטגרציה",
      "b2b_btn_2": "צור קשר עם המכירות",
      "loc_detecting": "מזהה את המיקום שלך...",
      "loc_found": "התוכנית הטובה ביותר לישראל:",
      "support_whatsapp": "תמיכה ב-WhatsApp",
      "search_placeholder": "לאן אתם טסים?",
      "popular_dest": "יעדים פופולריים",
      "app_title": "אפליקציית Connect.Global",
      "app_desc": "נהל את ה-eSIM שלך, עקוב אחר שימוש בנתונים בזמן אמת והטען מכל מקום בעולם.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "הפעלה מיידית",
          "desc": "לא נדרש SIM פיזי"
        },
        {
          "title": "תשלומים מאובטחים",
          "desc": "Apple Pay וקריפטו"
        },
        {
          "title": "מעקב נתונים",
          "desc": "ווידג'ט ל-iOS/Android"
        },
        {
          "title": "ריבוי מכשירים",
          "desc": "עד 5 eSIM פעילים"
        }
      ]
    },
    "testimonials": {
      "title": "המובילים בוטחים בנו",
      "items": [
        {
          "name": "ארי ל.",
          "role": "CTO @ Fintech Startup",
          "text": "האינטגרציה של ה-API הייתה חלקה. אנחנו מנהלים מעל 500 חיבורים עם אפס זמן השבתה."
        },
        {
          "name": "שרה מ.",
          "role": "CEO @ E-commerce Agency",
          "text": "סוף סוף ספק eSIM שמבין קנה מידה עסקי. המחירים הטובים ביותר לתעבורה ב-EU/US."
        }
      ]
    },
    "calculator": {
      "title": "מחשבון חיסכון B2B",
      "label": "שימוש בנתונים חודשיים",
      "saving": "אתה חוסך עד",
      "per_year": "בשנה"
    },
    "dashboard": {
      "title": "פעילות רשת חיה",
      "nodes": "צמתים פעילים",
      "traffic": "תעבורה נוכחית",
      "latency": "זמן תגובה",
      "status": "סטטוס מערכת: תקין",
      "israel_optimized": "מותאם לרשתות בישראל (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "נבנה עבור היי-טק וסטארטאפים",
      "desc": "תשתית מהימנה על ידי צוותים בתל אביב. הרחבה מיידית עבור סקриפינג, אוטומציה שיווקית ועבודה מרחוק.",
      "features": [
        "5G זמן תגובה נמוך",
        "גישת API ללא הגבלה",
        "חיוב ארגוני"
      ]
    },
    "stats": {
      "countries": "מדינות בכיסוי",
      "speed": "מהירות מקסימלית",
      "privacy": "פרטיות מלאה",
      "uptime": "התחייבות לזמינות"
    },
    "pricing": {
      "b2c_title": "חבילות נסיעה",
      "b2c_subtitle": "גיגה-בייט הוגנים במהירות מקסימלית. תעבורה שלא נוצלה פוקעת בסוף התקופה, מה שמאפשר לנו לשמור על המחירים הטובים ביותר.",
      "b2b_title": "תוכניות תשתית",
      "b2b_subtitle": "רכישת תעבורה בסיטונאות. חבר את המשתמשים שלך דרך ה-API שלנו. אתה משלם על המאגר המשותף, הלקוחות שלך משלמים לך.",
      "plans": {
        "light": {
          "name": "נוסע קל",
          "desc": "מושלם למפות והודעות לנסיעה קצרה."
        },
        "nomad": {
          "name": "נווד דיגיטלי",
          "desc": "מספיק לשיחות, עבודה и רשתות חברתיות לחודש שלם."
        },
        "ultra": {
          "name": "שידור אולטרה",
          "desc": "חופש מקסימלי. סטרימינג, וידאו 4K ושיתוף אינטרנט."
        },
        "startup": {
          "name": "מאגר סטארטאפ",
          "desc": "לצוותים קטנים ובדיקות ארביטראז'."
        },
        "agency": {
          "name": "קנה מידה של סוכנות",
          "desc": "לסוכנויות שיווק עם צриכה גבוהה."
        },
        "platform": {
          "name": "פלטפורמת API",
          "desc": "אינטגרציה לאפליקציה שלך (White Label)."
        }
      },
      "units": {
        "pack": "חבילה",
        "month": "חודש",
        "days": "ימים",
        "instant": "הפעלה מיידית (QR)",
        "hidden_fees": "ללא עמלות נסתרות",
        "hotspot": "שיתוף אינטרנט מותר",
        "traffic": "תעבורה",
        "api_access": "קוד גישה ל-API",
        "pool_ip": "מאגר IP ייעודי",
        "pool_label": "מאגר TB",
        "select": "בחר",
        "start": "התחל עבודה"
      }
    },
    "config": {
      "title": "הגדרת החבילה",
      "gb": "נתונים (GB)",
      "mins": "שיחות (דקות)",
      "sms": "חבילת SMS",
      "confirm": "המשך לתשלום",
      "total": "סה\"כ לחודש"
    },
    "checkout": {
      "title": "תשלום מאובטח",
      "step_final": "שלב אחרון",
      "apple_pay": "Apple Pay",
      "plan": "חבילה",
      "config": "הגדרה",
      "total_due": "סה\"כ לתשלום",
      "pay_now": "שלם עכשיו",
      "success": "ההפעלה הצליחה!",
      "success_desc": "ה-eSIM שלך מוכן. בדוק את האימייל שלך עבור קוד ה-QR.",
      "close": "סגור"
    },
    "footer": "Connect.Global © 2026. כל המערכות פועלות כסדרן."
  },
  "es": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "fr": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "de": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "zh": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ja": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ko": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "it": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "pt": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ar": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "hi": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "tr": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "nl": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "pl": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "fi": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "no": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "da": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "cs": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "el": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "id": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ms": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "th": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "vi": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "hu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ro": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sk": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "uk": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "bg": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "hr": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sr": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sl": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "et": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "lv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "lt": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "fa": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ur": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "bn": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ta": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "te": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "mr": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "gu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "kn": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ml": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "pa": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "am": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sw": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "af": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sq": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "hy": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "az": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "be": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "bs": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "my": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ca": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ceb": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ny": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "co": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "cy": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "eo": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "eu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "fy": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "gl": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ka": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ht": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ha": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "haw": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "is": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ig": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ga": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "jw": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "kk": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "km": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ku": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ky": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "lo": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "la": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "lb": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "mk": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "mg": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "mt": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "mi": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "mn": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ne": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ps": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sd": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "si": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "so": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "su": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "tg": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "uz": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "xh": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "yi": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "yo": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "zu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "fil": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ab": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "aa": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ak": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "an": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "av": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ay": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ba": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "bi": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ch": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "cv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "dz": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ee": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "fo": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "fj": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ff": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "gn": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "gv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ho": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "hz": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ia": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ie": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ik": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "io": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "iu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "kg": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ki": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "kj": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "kv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "kr": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "li": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ln": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "lu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "lg": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "mh": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "na": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "nd": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ng": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "nr": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "nv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "oc": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "oj": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "om": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "pi": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "qu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "rm": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "rn": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "rw": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sa": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sc": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "se": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sg": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sm": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sn": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "st": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ss": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ti": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "tk": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "tn": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "to": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ts": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "tt": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "tw": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ty": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ug": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ve": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "wa": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "wo": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "nso": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sh": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "dv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "gd": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "kw": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "br": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "os": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "ce": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "cu": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "tyv": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "sah": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  },
  "alt": {
    "nav": {
      "coverage": "Coverage",
      "pricing": "Pricing",
      "tech": "Technology",
      "api": "API"
    },
    "hero": {
      "b2c_tag": "Global roaming is cancelled",
      "b2c_title_1": "The World is Yours.",
      "b2c_title_2": "Just Connect.",
      "b2c_desc": "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      "b2c_btn_1": "Find Country",
      "b2c_btn_2": "Get the App",
      "b2b_tag": "Enterprise Class Traffic Infrastructure",
      "b2b_title_1": "Scalable",
      "b2b_title_2": "Connectivity Env.",
      "b2b_desc": "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      "b2b_btn_1": "Start Integration",
      "b2b_btn_2": "Contact Sales",
      "loc_detecting": "Detecting your location...",
      "loc_found": "Best plan for United Kingdom:",
      "support_whatsapp": "WhatsApp Support",
      "search_placeholder": "Where are you going?",
      "popular_dest": "Popular Destinations",
      "app_title": "The Connect.Global App",
      "app_desc": "Manage your eSIMs, track data usage in real-time, and top up instantly from anywhere in the world.",
      "app_ios": "App Store",
      "app_android": "Google Play",
      "app_features": [
        {
          "title": "Instant Activation",
          "desc": "No physical SIM needed"
        },
        {
          "title": "Secure Payments",
          "desc": "Apple Pay & Crypto"
        },
        {
          "title": "Data Tracking",
          "desc": "Widget for iOS/Android"
        },
        {
          "title": "Multi-device",
          "desc": "Up to 5 eSIMs active"
        }
      ]
    },
    "testimonials": {
      "title": "Trusted by the Best",
      "items": [
        {
          "name": "Ari L.",
          "role": "CTO @ Fintech Startup",
          "text": "The API integration was seamless. We manage over 500 connections with zero downtime."
        },
        {
          "name": "Sarah M.",
          "role": "CEO @ E-commerce Agency",
          "text": "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic."
        }
      ]
    },
    "calculator": {
      "title": "B2B ROI Calculator",
      "label": "Monthly Data Usage",
      "saving": "You save up to",
      "per_year": "per year"
    },
    "dashboard": {
      "title": "Live Network Activity",
      "nodes": "Active Nodes",
      "traffic": "Current Traffic",
      "latency": "Latency",
      "status": "System Status: Operational",
      "israel_optimized": "Optimized for IL Networks (Partner/Cellcom)"
    },
    "startup_section": {
      "title": "Built for Hi-Tech & Startups",
      "desc": "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
      "features": [
        "5G Low Latency",
        "Uncapped API Access",
        "Enterprise Billing"
      ]
    },
    "stats": {
      "countries": "Countries Covered",
      "speed": "Max Speed",
      "privacy": "Full Privacy",
      "uptime": "Uptime Guarantee"
    },
    "pricing": {
      "b2c_title": "Travel Packages",
      "b2c_subtitle": "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      "b2b_title": "Infrastructure Plans",
      "b2b_subtitle": "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      "plans": {
        "light": {
          "name": "Light Tripper",
          "desc": "Perfect for maps and messengers for a short trip."
        },
        "nomad": {
          "name": "Digital Nomad",
          "desc": "Enough for calls, work, and social media for a whole month."
        },
        "ultra": {
          "name": "Ultra Stream",
          "desc": "Maximum freedom. Streaming, 4K video, and hotspot tethering."
        },
        "startup": {
          "name": "Startup Pool",
          "desc": "For small teams and arbitrage tests."
        },
        "agency": {
          "name": "Agency Scale",
          "desc": "For marketing agencies with high consumption."
        },
        "platform": {
          "name": "Platform API",
          "desc": "Integration into your app (White Label)."
        }
      },
      "units": {
        "pack": "pack",
        "month": "mo",
        "days": "days",
        "instant": "Instant Activation (QR)",
        "hidden_fees": "No hidden fees",
        "hotspot": "Hotspot Allowed",
        "traffic": "Traffic",
        "api_access": "API Access Key",
        "pool_ip": "Dedicated IP Pool",
        "pool_label": "TB Pool",
        "select": "Select",
        "start": "Get Started"
      }
    },
    "config": {
      "title": "Configure Your Plan",
      "gb": "Data (GB)",
      "mins": "Voice (Mins)",
      "sms": "SMS Pack",
      "confirm": "Proceed to Checkout",
      "total": "Monthly Total"
    },
    "checkout": {
      "title": "Secure Checkout",
      "step_final": "Final Step",
      "apple_pay": "Apple Pay",
      "plan": "Plan",
      "config": "Configuration",
      "total_due": "Total Due",
      "pay_now": "Pay Now",
      "success": "Activation Successful!",
      "success_desc": "Your eSIM is ready. Check your email for the QR code.",
      "close": "Close"
    },
    "footer": "Connect.Global © 2026. All Systems Operational."
  }
};
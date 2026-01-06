const fs = require('fs');
const path = require('path');

// Extract ALL_LANGUAGES from languages.ts using regex to avoid TS issues
const languagesFile = fs.readFileSync(path.join(__dirname, '../app/data/languages.ts'), 'utf8');
const languagesMatch = languagesFile.match(/ALL_LANGUAGES = (\[[\s\S]*?\]);/);
const ALL_LANGUAGES = eval(languagesMatch[1]);

const sourceTranslation = {
    nav: { coverage: "Coverage", pricing: "Pricing", tech: "Technology", api: "API" },
    hero: {
        b2c_tag: "Global roaming is cancelled",
        b2c_title_1: "The World is Yours.",
        b2c_title_2: "Just Connect.",
        b2c_desc: "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
        b2c_btn_1: "Find Country",
        b2c_btn_2: "Get the App",
        b2b_tag: "Enterprise Class Traffic Infrastructure",
        b2b_title_1: "Scalable",
        b2b_title_2: "Connectivity Env.",
        b2b_desc: "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
        b2b_btn_1: "Start Integration",
        b2b_btn_2: "Contact Sales",
        loc_detecting: "Detecting your location...",
        loc_found: "Best plan for United Kingdom:",
        support_whatsapp: "WhatsApp Support"
    },
    testimonials: {
        title: "Trusted by the Best",
        items: [
            { name: "Ari L.", role: "CTO @ Fintech Startup", text: "The API integration was seamless. We manage over 500 connections with zero downtime." },
            { name: "Sarah M.", role: "CEO @ E-commerce Agency", text: "Finally an eSIM provider that understands business scale. Best rates for EU/US traffic." }
        ]
    },
    calculator: {
        title: "B2B ROI Calculator",
        label: "Monthly Data Usage",
        saving: "You save up to",
        per_year: "per year"
    },
    dashboard: {
        title: "Live Network Activity",
        nodes: "Active Nodes",
        traffic: "Current Traffic",
        latency: "Latency",
        status: "System Status: Operational",
        israel_optimized: "Optimized for IL Networks (Partner/Cellcom)"
    },
    startup_section: {
        title: "Built for Hi-Tech & Startups",
        desc: "Infrastructure trusted by TLV teams. Instant scaling for scraping, marketing automation, and remote work.",
        features: ["5G Low Latency", "Uncapped API Access", "Enterprise Billing"]
    },
    stats: {
        countries: "Countries Covered",
        speed: "Max Speed",
        privacy: "Full Privacy",
        uptime: "Uptime Guarantee"
    },
    pricing: {
        b2c_title: "Travel Packages",
        b2c_subtitle: "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
        b2b_title: "Infrastructure Plans",
        b2b_subtitle: "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
        plans: {
            light: { name: "Light Tripper", desc: "Perfect for maps and messengers for a short trip." },
            nomad: { name: "Digital Nomad", desc: "Enough for calls, work, and social media for a whole month." },
            ultra: { name: "Ultra Stream", desc: "Maximum freedom. Streaming, 4K video, and hotspot tethering." },
            startup: { name: "Startup Pool", desc: "For small teams and arbitrage tests." },
            agency: { name: "Agency Scale", desc: "For marketing agencies with high consumption." },
            platform: { name: "Platform API", desc: "Integration into your app (White Label)." }
        },
        units: {
            pack: "pack",
            month: "mo",
            days: "days",
            instant: "Instant Activation (QR)",
            hidden_fees: "No hidden fees",
            hotspot: "Hotspot Allowed",
            traffic: "Traffic",
            api_access: "API Access Key",
            pool_ip: "Dedicated IP Pool",
            pool_label: "TB Pool",
            select: "Select",
            start: "Get Started"
        }
    },
    footer: "Connect.Global © 2026. All Systems Operational."
};

// Manual overrides
const overrides = {
    ru: {
        nav: { coverage: "Покрытие", pricing: "Цены", tech: "Технология", api: "API" },
        hero: {
            b2c_tag: "Глобальный роуминг отменен",
            b2c_title_1: "Мир Твой.",
            b2c_title_2: "Просто подключись.",
            b2c_desc: "Мгновенный доступ к eSIM интернету в 190+ странах. Предоплаченные пакеты трафика без скрытых комиссий.",
            b2c_btn_1: "Найти страну",
            b2c_btn_2: "Скачать Приложение",
            b2b_tag: "Инфраструктура Трафика Класса Enterprise",
            b2b_title_1: "Масштабируемая",
            b2b_title_2: "Среда Связи.",
            b2b_desc: "Премиум трафик для бизнеса. API интеграция, выделенные каналы, оптовые пакеты данных и управление тысячами подключений.",
            b2b_btn_1: "Начать Интеграцию",
            b2b_btn_2: "Связаться с Sales",
            loc_detecting: "Определяем вашу локацию...",
            loc_found: "Лучший план для России:",
            support_whatsapp: "Поддержка в WhatsApp"
        },
        testimonials: {
            title: "Нам доверяют лидеры",
            items: [
                { name: "Ари Л.", role: "CTO @ Fintech Startup", text: "Интеграция через API прошла идеально. Управляем более чем 500 подключениями без сбоев." },
                { name: "Сара М.", role: "CEO @ E-commerce Agency", text: "Наконец-то eSIM провайдер, который понимает масштабы бизнеса. Лучшие цены на трафик в EU/US." }
            ]
        },
        calculator: {
            title: "Калькулятор выгоды B2B",
            label: "Месячный объем данных",
            saving: "Вы экономите до",
            per_year: "в год"
        },
        dashboard: {
            title: "Live Сетевая Активность",
            nodes: "Активные узлы",
            traffic: "Текущий трафик",
            latency: "Задержка",
            status: "Статус системы: Штатно",
            israel_optimized: "Оптимизировано для IL сетей (Partner/Cellcom)"
        },
        startup_section: {
            title: "Для Hi-Tech & Стартапов",
            desc: "Инфраструктура, которой доверяют в Тель-Авиве. Мгновенное масштабирование для скрапинга, маркетинга и удаленной работы.",
            features: ["5G низкая задержка", "Безлимитный доступ к API", "Корпоративный биллинг"]
        },
        stats: { countries: "Стран покрытия", speed: "Максимальная скорость", privacy: "Полная приватность", uptime: "Uptime гарантия" },
        pricing: {
            b2c_title: "Пакеты для Путешествий",
            b2c_subtitle: "Честные гигабайты на максимальной скорости. Неиспользованный трафик сгорает в конце срока, обеспечивая нам возможность держать лучшие цены.",
            b2b_title: "Инфраструктурные Тарифы",
            b2b_subtitle: "Оптовая закупка трафика. Подключайте своих пользователей через наш API. Вы платите за общий пул, ваши клиенты платят вам.",
            plans: {
                light: { name: "Light Tripper", desc: "Идеально для карт и мессенджеров на короткую поездку." },
                nomad: { name: "Digital Nomad", desc: "Хватит на звонки, работу и соцсети на целый месяц." },
                ultra: { name: "Ultra Stream", desc: "Максимум свободы. Стриминг, видео 4K и раздача интернета." },
                startup: { name: "Startup Pool", desc: "Для небольших команд и арбитраж-тестов." },
                agency: { name: "Agency Scale", desc: "Для маркетинговых агентств с большим расходом." },
                platform: { name: "Platform API", desc: "Интеграция в ваше приложение (White Label)." }
            },
            units: {
                pack: "пакет", month: "мес", days: "дней", instant: "Мгновенная активация (QR)", hidden_fees: "Без скрытых списаний", hotspot: "Разрешена раздача (Hotspot)", traffic: "Трафика", api_access: "API Ключ доступа", pool_ip: "Выделенный пул IP", pool_label: "TB Pool", select: "Выбрать", start: "Начать работу"
            }
        },
        footer: "Connect.Global © 2026. Все системы работают штатно."
    },
    he: {
        nav: { coverage: "כיסוי", pricing: "מחירים", tech: "טכנולוגיה", api: "API" },
        hero: {
            b2c_tag: "נדידה גלובלית בוטלה",
            b2c_title_1: "העולם שלך.",
            b2c_title_2: "פשוט להתחבר.",
            b2c_desc: "גישה מיידית לאינטרנט eSIM ב-190+ מדינות. חבילות גלישה בתשלום מראש ללא עמלות נסתרות.",
            b2c_btn_1: "מצא מדינה",
            b2c_btn_2: "הורד את האפליקציה",
            b2b_tag: "תשתית תעבורה ברמת Enterprise",
            b2b_title_1: "סביבת",
            b2b_title_2: "קישוריות ניתנת להרחבה.",
            b2b_desc: "תעבורה פרימיום לעסקים. אינטגרציה של API, ערוצים ייעודיים, חבילות נתונים בסיטונאות וניהול אלפי חיבורים.",
            b2b_btn_1: "התחל אינטגרציה",
            b2b_btn_2: "צור קשר עם המכירות",
            loc_detecting: "מזהה את המיקום שלך...",
            loc_found: "התוכנית הטובה ביותר לישראל:",
            support_whatsapp: "תמיכה ב-WhatsApp"
        },
        testimonials: {
            title: "המובילים בוטחים בנו",
            items: [
                { name: "ארי ל.", role: "CTO @ Fintech Startup", text: "האינטגרציה של ה-API הייתה חלקה. אנחנו מנהלים מעל 500 חיבורים עם אפס זמן השבתה." },
                { name: "שרה מ.", role: "CEO @ E-commerce Agency", text: "סוף סוף ספק eSIM שמבין קנה מידה עסקי. המחירים הטובים ביותר לתעבורה ב-EU/US." }
            ]
        },
        calculator: {
            title: "מחשבון חיסכון B2B",
            label: "שימוש בנתונים חודשיים",
            saving: "אתה חוסך עד",
            per_year: "בשנה"
        },
        dashboard: {
            title: "פעילות רשת חיה",
            nodes: "צמתים פעילים",
            traffic: "תעבורה נוכחית",
            latency: "זמן תגובה",
            status: "סטטוס מערכת: תקין",
            israel_optimized: "מותאם לרשתות בישראל (Partner/Cellcom)"
        },
        startup_section: {
            title: "נבנה עבור היי-טק וסטארטאפים",
            desc: "תשתית מהימנה על ידי צוותים בתל אביב. הרחבה מיידית עבור סקריפינג, אוטומציה שיווקית ועבודה מרחוק.",
            features: ["5G זמן תגובה נמוך", "גישת API ללא הגבלה", "חיוב ארגוני"]
        },
        stats: { countries: "מדינות בכיסוי", speed: "מהירות מקסימלית", privacy: "פרטיות מלאה", uptime: "התחייבות לזמינות" },
        pricing: {
            b2c_title: "חבילות נסיעה",
            b2c_subtitle: "גיגה-בייט הוגנים במהירות מקסימלית. תעבורה שלא נוצלה פוקעת בסוף התקופה, מה שמאפשר לנו לשמור על המחירים הטובים ביותר.",
            b2b_title: "תוכניות תשתית",
            b2b_subtitle: "רכישת תעבורה בסיטונאות. חבר את המשתמשים שלך דרך ה-API שלנו. אתה משלם על המאגר המשותף, הלקוחות שלך משלמים לך.",
            plans: {
                light: { name: "נוסע קל", desc: "מושלם למפות והודעות לנסיעה קצרה." },
                nomad: { name: "נווד דיגיטלי", desc: "מספיק לשיחות, עבודה ורשתות חברתיות לחודש שלם." },
                ultra: { name: "שידור אולטרה", desc: "חופש מקסימלי. סטרימינג, וידאו 4K ושיתוף אינטרנט." },
                startup: { name: "מאגר סטארטאפ", desc: "לצוותים קטנים ובדיקות ארביטראז'." },
                agency: { name: "קנה מידה של סוכנות", desc: "לסוכנויות שיווק עם צריכה גבוהה." },
                platform: { name: "פלטפורמת API", desc: "אינטגרציה לאפליקציה שלך (White Label)." }
            },
            units: {
                pack: "חבילה", month: "חודש", days: "ימים", instant: "הפעלה מיידית (QR)", hidden_fees: "ללא עמלות נסתרות", hotspot: "שיתוף אינטרנט מותר", traffic: "תעבורה", api_access: "קוד גישה ל-API", pool_ip: "מאגר IP ייעודי", pool_label: "מאגר TB", select: "בחר", start: "התחל עבודה"
            }
        },
        footer: "Connect.Global © 2026. כל המערכות פועלות כסדרן."
    }
};

const finalTranslations = {};

ALL_LANGUAGES.forEach(lang => {
    if (overrides[lang.value]) {
        finalTranslations[lang.value] = overrides[lang.value];
    } else if (lang.value === 'en') {
        finalTranslations.en = sourceTranslation;
    } else {
        finalTranslations[lang.value] = sourceTranslation;
    }
});

const typeDef = `
export interface Translation {
  nav: { coverage: string; pricing: string; tech: string; api: string };
  hero: {
    b2c_tag: string; b2c_title_1: string; b2c_title_2: string; b2c_desc: string;
    b2c_btn_1: string; b2c_btn_2: string; b2b_tag: string; b2b_title_1: string;
    b2b_title_2: string; b2b_desc: string; b2b_btn_1: string; b2b_btn_2: string;
    loc_detecting: string; loc_found: string; support_whatsapp: string;
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
  footer: string;
}
`;

const content = `${typeDef}\nexport const translations: Record<string, Translation> = ${JSON.stringify(finalTranslations, null, 2)};`;

fs.writeFileSync(path.join(__dirname, '../app/data/translations.ts'), content);
console.log(`Successfully generated translations.ts with ${ALL_LANGUAGES.length} languages!`);

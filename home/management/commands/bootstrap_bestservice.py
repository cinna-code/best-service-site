from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from wagtail.images import get_image_model
from wagtail.models import Page, Site

from home.models import (
    Certificate,
    HeroSystemNode,
    HomePage,
    ITFeature,
    NavigationItem,
    Partner,
    ResultBenefit,
    ServiceCard,
    SiteSettings,
    TickerItem,
)


ASSET_DIR = Path(__file__).resolve().parents[2] / "static" / "home"


class Command(BaseCommand):
    help = "Creates the Best Service home page and imports the supplied logo assets."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Replace existing CMS content with the supplied Best Service starter content.",
        )

    def handle(self, *args, **options):
        refresh = options["refresh"]
        page = HomePage.objects.first()
        created = page is None

        defaults = {
            "hero_eyebrow": "ИТ-ИНФРАСТРУКТУРА ДЛЯ БИЗНЕСА",
            "hero_title_line": "Бизнес работает.",
            "hero_title_accent": "Мы держим IT.",
            "hero_lead": "Автоматизируем процессы, внедряем ПО и обеспечиваем бесперебойную работу инфраструктуры — от 1С до торгового оборудования.",
            "hero_primary_label": "Получить консультацию",
            "hero_primary_link": "#contact",
            "hero_secondary_label": "Посмотреть услуги",
            "hero_secondary_link": "#services",
            "hero_line_number": "01",
            "hero_line_left": "ОТ ПО ДО ОБОРУДОВАНИЯ",
            "hero_line_right": "ОДИН ПАРТНЁР ДЛЯ ВАШЕГО IT",
            "core_label": "IT",
            "core_subtitle": "под ключ",
            "visual_caption_line_one": "Единая система.",
            "visual_caption_line_two": "Управляемый результат.",
            "navigation_aria_label": "Главное меню",
            "hero_visual_aria_label": "Схема единой IT-системы",
            "ticker_aria_label": "Направления работы",
            "certificates_aria_label": "Галерея сертификатов",
            "overview_eyebrow": "ПОЛНОЕ IT-СОПРОВОЖДЕНИЕ",
            "overview_title_line": "IT-среда, в которой",
            "overview_title_accent": "всё под контролем.",
            "overview_body": "Это не просто компьютеры и программы. Мы связываем в единую рабочую систему офис, склад, торговые точки, сотрудников и данные — а затем поддерживаем её каждый день.",
            "services_eyebrow": "ЧТО ДЕЛАЕМ",
            "services_title_line": "Вся IT-среда —",
            "services_title_accent": "в надёжных руках.",
            "services_body": "Берём на себя внедрение, настройку и поддержку, чтобы ваши сотрудники занимались бизнесом, а не техническими сбоями.",
            "result_eyebrow": "ЦЕННЫЙ КОНЕЧНЫЙ ПРОДУКТ",
            "result_title_line": "IT, которое",
            "result_title_accent": "не отвлекает.",
            "result_intro": "Best Service — автоматизированный, управляемый и безопасный бизнес клиента, работающий без сбоев.",
            "partners_eyebrow": "ОФИЦИАЛЬНОЕ ПАРТНЁРСТВО",
            "partners_body": "Работаем с проверенными технологиями и отвечаем за результат на каждом этапе.",
            "certificates_eyebrow": "ДОКУМЕНТЫ И СТАТУСЫ",
            "certificates_title_line": "Подтверждённая",
            "certificates_title_accent": "экспертиза.",
            "certificates_body": "Официальные документы подтверждают квалификацию команды и статус партнёра Best Service.",
            "contact_eyebrow": "НАЧНЁМ С ДИАГНОСТИКИ",
            "contact_title_line": "Пора навести",
            "contact_title_accent": "порядок в IT.",
            "contact_button_label": "НАПИСАТЬ\nНАМ",
            "contact_button_link": "#top",
            "contact_note": "Расскажите о своей задаче — предложим понятный план решения. Контакты добавим при финализации.",
            "search_description": "Best Service — IT под ключ: автоматизация, сопровождение ПО и торговое оборудование Zebra.",
            "seo_title": "Best Service — IT под ключ",
        }

        if created:
            # A stock Wagtail installation reserves the `home` slug for its
            # welcome page. The Site root below makes this page available at
            # `/`, so the internal slug never appears to visitors.
            page = HomePage(title="Best Service", slug="best-service", **defaults)
            Page.get_first_root_node().add_child(instance=page)
        elif refresh:
            for field, value in defaults.items():
                setattr(page, field, value)
            page.save()

        site = Site.objects.filter(is_default_site=True).first()
        if site is None:
            site = Site.objects.create(
                hostname="localhost",
                port=8000,
                root_page=page,
                site_name="Best Service",
                is_default_site=True,
            )
        else:
            site.root_page = page
            site.site_name = "Best Service"
            site.save()

        logo = self._image("Best Service — логотип", "best-service-logo-transparent.png")
        logo_1c = self._image("1С — логотип", "1s-logo.png")
        logo_bitrix = self._image("Bitrix24 — логотип", "bitrix24-logo-eng.png")
        logo_zebra = self._image("Zebra — логотип", "zebra-logo2.png")
        settings = SiteSettings.for_site(site)
        if created or refresh:
            settings.logo = logo
            settings.logo_alt = "Best Service"
            settings.header_cta_label = "Обсудить задачу"
            settings.header_cta_link = "#contact"
            settings.footer_tagline = "IT под ключ для бизнеса"
            settings.copyright_text = "© 2026 Best Service"
            settings.save()

            self._replace_inline_content(page, logo_1c, logo_bitrix, logo_zebra)
            page.save_revision().publish()

        message = "создана" if created else "обновлена" if refresh else "уже существует"
        self.stdout.write(self.style.SUCCESS(f"Главная страница Best Service {message}."))

    def _image(self, title, filename):
        image_model = get_image_model()
        existing = image_model.objects.filter(title=title).first()
        if existing:
            return existing

        asset = ASSET_DIR / filename
        with asset.open("rb") as source:
            return image_model.objects.create(title=title, file=File(source, name=filename))

    def _replace_inline_content(self, page, logo_1c, logo_bitrix, logo_zebra):
        for manager in [
            page.navigation_items,
            page.ticker_items,
            page.hero_nodes,
            page.it_features,
            page.service_cards,
            page.result_benefits,
            page.partners,
            page.certificates,
        ]:
            manager.all().delete()

        for label, anchor in [
            ("Услуги", "#services"),
            ("Результат", "#result"),
            ("Партнёры", "#partners"),
            ("Сертификаты", "#certificates"),
        ]:
            NavigationItem.objects.create(page=page, label=label, anchor=anchor)

        for label in [
            "1С",
            "БИТРИКС24",
            "WMS / TMS",
            "ZEBRA",
            "DATAMOBILE",
            "МОБИ-С",
            "SMARTAPP",
            "АГЕНТ+",
            "МОБИЛЬНЫЕ ПРИЛОЖЕНИЯ",
            "IT-СОПРОВОЖДЕНИЕ",
        ]:
            TickerItem.objects.create(page=page, label=label)

        for label, position in [
            ("1С", "top"),
            ("WMS", "left"),
            ("TMS", "right"),
            ("CRM", "bottom"),
            ("МП", "mobile"),
        ]:
            HeroSystemNode.objects.create(page=page, label=label, position=position)

        for number, title, body in [
            ("01", "Инфраструктура и сети", "Проектируем и обслуживаем рабочие места, серверы, Wi-Fi, локальные сети и облачные сервисы. Новые филиалы и точки подключаем без хаоса в работе."),
            ("02", "Защита и сохранность данных", "Настраиваем резервное копирование, права доступа, антивирусную защиту и мониторинг. Важная информация остаётся доступной и защищённой."),
            ("03", "Поддержка сотрудников", "Помогаем пользователям удалённо и на месте: от настройки рабочего места и почты до устранения сбоев. Берём вопросы IT в одно окно."),
            ("04", "IT для торговли и склада", "Интегрируем 1С, Битрикс, WMS/TMS и мобильные решения с принтерами, ТСД и сканерами Zebra. Все процессы работают как единая цепочка."),
        ]:
            ITFeature.objects.create(page=page, number=number, title=title, body=body)

        for number, icon, first_line, second_line, body, featured in [
            ("01", "⌘", "Автоматизация", "бизнеса", "Внедрение и сопровождение 1С, Битрикс, WMS и TMS. Настраиваем процессы под вашу реальную работу.", True),
            ("02", "◫", "Мобильные", "решения", "Агент+, SmartApp, Моби-С и DataMobile — для продаж, склада и работы команды в поле.", False),
            ("03", "◌", "Техническое", "сопровождение", "Полное обслуживание IT-инфраструктуры и торгового оборудования без простоев.", False),
            ("04", "▦", "Оборудование", "Zebra", "Подберём, привезём и установим любое решение Zebra как официальный дилер.", False),
        ]:
            ServiceCard.objects.create(
                page=page,
                number=number,
                icon=icon,
                title_line_one=first_line,
                title_line_two=second_line,
                body=body,
                cta_label="Подробнее",
                cta_link="#contact",
                is_featured=featured,
            )

        for text in [
            "Бесперебойная работа IT-систем без простоев и потерь данных",
            "Полностью настроенная и обслуживаемая инфраструктура «под ключ»",
            "Стабильные процессы, которыми легко управлять",
        ]:
            ResultBenefit.objects.create(page=page, text=text)

        for name, logo, alt in [
            ("1С", logo_1c, "Логотип 1С"),
            ("Bitrix24", logo_bitrix, "Логотип Bitrix24"),
            ("Zebra", logo_zebra, "Логотип Zebra"),
        ]:
            Partner.objects.create(page=page, name=name, logo=logo, alt_text=alt)

        for number, title, is_landscape in [
            ("01", "Сертификат «1С:Профессионал»", False),
            ("02", "Сертификат партнёра 1С, 2025", False),
            ("03", "Официальный партнёр 1С", False),
            ("04", "Торгово-складской функционал: УТ, КА и 1С:ERP", False),
            ("05", "Управленческое лидерство", False),
            ("06", "1С:Специалист — разработка и модификация", False),
            ("07", "1С:Специалист — внедрение торговых решений", False),
            ("08", "1С:Профессионал — торговля", False),
            ("09", "Функциональный архитектор 1С", True),
            ("10", "CAP — сертифицированный бухгалтер-практик", True),
        ]:
            Certificate.objects.create(
                page=page,
                number=number,
                title=title,
                status=title,
                is_landscape=is_landscape,
            )

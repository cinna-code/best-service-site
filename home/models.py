from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Orderable, Page


@register_setting
class SiteSettings(BaseSiteSetting):
    """Reusable brand and footer content, edited under Settings in Wagtail."""

    logo = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип",
    )
    logo_alt = models.CharField("Описание логотипа", max_length=255, default="Best Service")
    header_cta_label = models.CharField("Текст кнопки в шапке", max_length=100, default="Обсудить задачу")
    header_cta_link = models.CharField("Ссылка кнопки в шапке", max_length=255, default="#contact")
    footer_tagline = models.CharField("Текст в подвале", max_length=255, default="IT под ключ для бизнеса")
    copyright_text = models.CharField("Копирайт", max_length=255, default="© 2026 Best Service")

    panels = [
        MultiFieldPanel(
            [FieldPanel("logo"), FieldPanel("logo_alt")],
            heading="Логотип",
        ),
        MultiFieldPanel(
            [FieldPanel("header_cta_label"), FieldPanel("header_cta_link")],
            heading="Кнопка в шапке",
        ),
        MultiFieldPanel(
            [FieldPanel("footer_tagline"), FieldPanel("copyright_text")],
            heading="Подвал",
        ),
    ]

    class Meta:
        verbose_name = "Настройки Best Service"


class HomePage(Page):
    """One editable page preserving the current Best Service design."""

    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    # Hero
    hero_eyebrow = models.CharField("Надпись над главным заголовком", max_length=255)
    hero_title_line = models.CharField("Главный заголовок — первая строка", max_length=255)
    hero_title_accent = models.CharField("Главный заголовок — цветная строка", max_length=255)
    hero_lead = models.TextField("Описание под главным заголовком")
    hero_primary_label = models.CharField("Текст основной кнопки", max_length=100)
    hero_primary_link = models.CharField("Ссылка основной кнопки", max_length=255, default="#contact")
    hero_secondary_label = models.CharField("Текст дополнительной ссылки", max_length=100)
    hero_secondary_link = models.CharField("Ссылка дополнительной ссылки", max_length=255, default="#services")
    hero_line_number = models.CharField("Номер в строке под первым экраном", max_length=12, default="01")
    hero_line_left = models.CharField("Левая часть строки под первым экраном", max_length=255)
    hero_line_right = models.CharField("Правая часть строки под первым экраном", max_length=255)
    core_label = models.CharField("Текст в центре схемы", max_length=32, default="IT")
    core_subtitle = models.CharField("Подпись в центре схемы", max_length=100, default="под ключ")
    visual_caption_line_one = models.CharField("Подпись схемы — строка 1", max_length=100)
    visual_caption_line_two = models.CharField("Подпись схемы — строка 2", max_length=100)
    navigation_aria_label = models.CharField("Описание главного меню для экранных читалок", max_length=255, default="Главное меню")
    hero_visual_aria_label = models.CharField("Описание схемы для экранных читалок", max_length=255, default="Схема единой IT-системы")
    ticker_aria_label = models.CharField("Описание бегущей строки для экранных читалок", max_length=255, default="Направления работы")
    certificates_aria_label = models.CharField("Описание галереи сертификатов для экранных читалок", max_length=255, default="Галерея сертификатов")

    # Overview
    overview_eyebrow = models.CharField("IT-сопровождение — надпись", max_length=255)
    overview_title_line = models.CharField("IT-сопровождение — первая строка", max_length=255)
    overview_title_accent = models.CharField("IT-сопровождение — цветная строка", max_length=255)
    overview_body = models.TextField("IT-сопровождение — описание")

    # Services
    services_eyebrow = models.CharField("Услуги — надпись", max_length=255)
    services_title_line = models.CharField("Услуги — первая строка", max_length=255)
    services_title_accent = models.CharField("Услуги — цветная строка", max_length=255)
    services_body = models.TextField("Услуги — описание")

    # Result
    result_eyebrow = models.CharField("Результат — надпись", max_length=255)
    result_title_line = models.CharField("Результат — первая строка", max_length=255)
    result_title_accent = models.CharField("Результат — цветная строка", max_length=255)
    result_intro = models.TextField("Результат — главное описание")

    # Partners
    partners_eyebrow = models.CharField("Партнёры — надпись", max_length=255)
    partners_body = models.TextField("Партнёры — описание")

    # Certificates
    certificates_eyebrow = models.CharField("Сертификаты — надпись", max_length=255)
    certificates_title_line = models.CharField("Сертификаты — первая строка", max_length=255)
    certificates_title_accent = models.CharField("Сертификаты — цветная строка", max_length=255)
    certificates_body = models.TextField("Сертификаты — описание")

    # Contact
    contact_eyebrow = models.CharField("Контакты — надпись", max_length=255)
    contact_title_line = models.CharField("Контакты — первая строка", max_length=255)
    contact_title_accent = models.CharField("Контакты — цветная строка", max_length=255)
    contact_button_label = models.CharField("Контакты — текст кнопки", max_length=100)
    contact_button_link = models.CharField("Контакты — ссылка кнопки", max_length=255, default="#top")
    contact_note = models.TextField("Контакты — пояснение")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_eyebrow"),
                FieldPanel("hero_title_line"),
                FieldPanel("hero_title_accent"),
                FieldPanel("hero_lead"),
                FieldPanel("hero_primary_label"),
                FieldPanel("hero_primary_link"),
                FieldPanel("hero_secondary_label"),
                FieldPanel("hero_secondary_link"),
            ],
            heading="Первый экран",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hero_line_number"),
                FieldPanel("hero_line_left"),
                FieldPanel("hero_line_right"),
                FieldPanel("core_label"),
                FieldPanel("core_subtitle"),
                FieldPanel("visual_caption_line_one"),
                FieldPanel("visual_caption_line_two"),
                FieldPanel("hero_visual_aria_label"),
                InlinePanel("hero_nodes", label="Элемент схемы"),
            ],
            heading="Схема IT и строка под первым экраном",
        ),
        MultiFieldPanel(
            [FieldPanel("navigation_aria_label"), InlinePanel("navigation_items", label="Пункт меню")],
            heading="Навигация",
        ),
        MultiFieldPanel(
            [FieldPanel("ticker_aria_label"), InlinePanel("ticker_items", label="Пункт бегущей строки")],
            heading="Бегущая строка",
        ),
        MultiFieldPanel(
            [
                FieldPanel("overview_eyebrow"),
                FieldPanel("overview_title_line"),
                FieldPanel("overview_title_accent"),
                FieldPanel("overview_body"),
                InlinePanel("it_features", label="Карточка IT-сопровождения"),
            ],
            heading="Полное IT-сопровождение",
        ),
        MultiFieldPanel(
            [
                FieldPanel("services_eyebrow"),
                FieldPanel("services_title_line"),
                FieldPanel("services_title_accent"),
                FieldPanel("services_body"),
                InlinePanel("service_cards", label="Карточка услуги"),
            ],
            heading="Услуги",
        ),
        MultiFieldPanel(
            [
                FieldPanel("result_eyebrow"),
                FieldPanel("result_title_line"),
                FieldPanel("result_title_accent"),
                FieldPanel("result_intro"),
                InlinePanel("result_benefits", label="Пункт результата"),
            ],
            heading="Результат",
        ),
        MultiFieldPanel(
            [FieldPanel("partners_eyebrow"), FieldPanel("partners_body"), InlinePanel("partners", label="Партнёр")],
            heading="Партнёры",
        ),
        MultiFieldPanel(
            [
                FieldPanel("certificates_eyebrow"),
                FieldPanel("certificates_title_line"),
                FieldPanel("certificates_title_accent"),
                FieldPanel("certificates_body"),
                FieldPanel("certificates_aria_label"),
                InlinePanel("certificates", label="Сертификат"),
            ],
            heading="Сертификаты и документы",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_eyebrow"),
                FieldPanel("contact_title_line"),
                FieldPanel("contact_title_accent"),
                FieldPanel("contact_button_label"),
                FieldPanel("contact_button_link"),
                FieldPanel("contact_note"),
            ],
            heading="Контактный блок",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["site_settings"] = SiteSettings.for_request(request)
        context["portrait_certificates"] = self.certificates.filter(
            show_on_site=True,
            is_landscape=False,
        )
        context["landscape_certificates"] = self.certificates.filter(
            show_on_site=True,
            is_landscape=True,
        )
        return context


class NavigationItem(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="navigation_items")
    label = models.CharField("Текст пункта меню", max_length=100)
    anchor = models.CharField("Ссылка или якорь", max_length=255, help_text="Например: #services")
    panels = [FieldPanel("label"), FieldPanel("anchor")]


class TickerItem(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="ticker_items")
    label = models.CharField("Текст", max_length=100)
    panels = [FieldPanel("label")]


class HeroSystemNode(Orderable):
    POSITION_CHOICES = [
        ("top", "Сверху"),
        ("right", "Справа"),
        ("bottom", "Снизу"),
        ("left", "Слева"),
        ("mobile", "Сверху справа (Mobile Apps)"),
    ]
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="hero_nodes")
    label = models.TextField("Текст узла", max_length=100, help_text="Перенос строки можно сделать клавишей Enter.")
    position = models.CharField("Расположение", max_length=20, choices=POSITION_CHOICES)
    panels = [FieldPanel("label"), FieldPanel("position")]


class ITFeature(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="it_features")
    number = models.CharField("Номер", max_length=12)
    title = models.CharField("Заголовок", max_length=255)
    body = models.TextField("Описание")
    panels = [FieldPanel("number"), FieldPanel("title"), FieldPanel("body")]


class ServiceCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="service_cards")
    number = models.CharField("Номер", max_length=12)
    icon = models.CharField("Символ иконки", max_length=16, default="⌘")
    title_line_one = models.CharField("Заголовок — строка 1", max_length=100)
    title_line_two = models.CharField("Заголовок — строка 2", max_length=100, blank=True)
    body = models.TextField("Описание")
    cta_label = models.CharField("Текст ссылки", max_length=100, default="Подробнее")
    cta_link = models.CharField("Ссылка", max_length=255, default="#contact")
    is_featured = models.BooleanField("Выделить карточку", default=False)
    panels = [
        FieldPanel("number"),
        FieldPanel("icon"),
        FieldPanel("title_line_one"),
        FieldPanel("title_line_two"),
        FieldPanel("body"),
        FieldPanel("cta_label"),
        FieldPanel("cta_link"),
        FieldPanel("is_featured"),
    ]


class ResultBenefit(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="result_benefits")
    text = models.CharField("Текст пункта", max_length=500)
    panels = [FieldPanel("text")]


class Partner(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="partners")
    name = models.CharField("Название партнёра", max_length=100)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Логотип",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    alt_text = models.CharField("Описание логотипа", max_length=255)
    link = models.CharField("Ссылка", max_length=255, blank=True)
    panels = [FieldPanel("name"), FieldPanel("logo"), FieldPanel("alt_text"), FieldPanel("link")]


class Certificate(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="certificates")
    number = models.CharField("Номер", max_length=12)
    is_landscape = models.BooleanField(
        "Горизонтальный формат",
        default=False,
        help_text="Включите для горизонтального сертификата: он появится отдельной строкой из двух карточек.",
    )
    title = models.CharField("Название документа", max_length=255)
    issuer = models.CharField("Кем выдан / подпись", max_length=255, blank=True)
    status = models.CharField("Статус или дополнительная подпись", max_length=255, blank=True)
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Превью документа",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    document = models.ForeignKey(
        "wagtaildocs.Document",
        verbose_name="Файл для скачивания",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    external_link = models.URLField("Внешняя ссылка", blank=True)
    show_on_site = models.BooleanField("Показывать на сайте", default=True)
    panels = [
        FieldPanel("number"),
        FieldPanel("is_landscape"),
        FieldPanel("title"),
        FieldPanel("issuer"),
        FieldPanel("status"),
        FieldPanel("thumbnail"),
        FieldPanel("document"),
        FieldPanel("external_link"),
        FieldPanel("show_on_site"),
    ]

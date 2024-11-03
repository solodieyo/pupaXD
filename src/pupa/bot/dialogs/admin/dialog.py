from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, StartMode, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
	SwitchTo,
	Row,
	Start,
	Group,
	Select,
	Button,
	ScrollingGroup,
	PrevPage,
	NextPage
)
from aiogram_dialog.widgets.text import Const, Format

from pupa.bot.dialogs.admin.getters import (
	getter_themes,
	themes_item_id_getter,
	getter_questions,
	questions_item_id_getter,
	getter_question
)
from pupa.bot.dialogs.admin.handlers import (
	on_select_theme,
	on_delete_theme,
	on_select_question,
	on_delete_question,
	on_change_answer,
	on_change_question_text,
	on_change_question_media,
	on_change_question_media_and_text,
	on_create_question_text,
	on_create_question_media,
	on_create_question_answer
)
from pupa.bot.states.dialog_states import AdminMenuStates, SettingsStates

admin_menu = Window(
	Const('🅰️ Админ меню'),
	Row(
		Start(
			text=Const('Статистика'),
			id='statistics',
			state=AdminMenuStates.stats
		),
		SwitchTo(
			text=Const('Темы'),
			id='themes',
			state=AdminMenuStates.themes_select
		),
	),
	Start(
		text=Const('Назад'),
		state=SettingsStates.main,
		id='back_to_main',
		mode=StartMode.RESET_STACK
	),
	state=AdminMenuStates.main
)

theme_select = Window(
	Const('Выберите тему'),
	Group(
		Select(
			text=Format('{item.theme_name}'),
			id='theme_select',
			items='themes',
			item_id_getter=themes_item_id_getter,
			type_factory=int,
			on_click=on_select_theme
		),
		width=2,
	),
	SwitchTo(
		text=Const('➕ Создать новую тему'),
		id='add_theme',
		state=AdminMenuStates.add_theme
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.main,
		id='back_to_main',
	),
	state=AdminMenuStates.themes_select,
	getter=getter_themes
)

theme_manage = Window(
	Const('Управление темой'),
	SwitchTo(
		text=Const('➕ Добавить новый вопрос'),
		id='add_theme',
		state=AdminMenuStates.add_question
	),
	SwitchTo(
		text=Const('Вопросы'),
		id='questions',
		state=AdminMenuStates.manage_theme_questions
	),
	SwitchTo(
		text=Const('Удалить тему'),
		id='delete_theme',
		state=AdminMenuStates.delete_theme_confirm
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.themes_select,
		id='back_to_themes'
	),
	state=AdminMenuStates.manage_theme
)

delete_theme = Window(
	Const('Удалить тему?'),
	Button(
		text=Const('Да, удалить'),
		id='delete_theme',
		on_click=on_delete_theme
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.manage_theme,
		id='back_to_manage'
	),
	state=AdminMenuStates.delete_theme_confirm
)

questions = Window(
	Const('Выберите вопрос для редактирования'),
	ScrollingGroup(
		Select(
			text=Format('{item.answer}'),
			id='question_select',
			items='questions',
			item_id_getter=questions_item_id_getter,
			type_factory=int,
			on_click=on_select_question
		),
		width=2,
		height=5,
		id='questions_scroll'
	),
	Row(
		PrevPage(
			scroll="questions_scroll", text=Format("👈 Предыдущие"),
			when=F["pages"] > 1 & F["current_page1"] != 1
		),
		NextPage(
			scroll="questions_scroll", text=Format("👉 Следующие"),
			when=F["current_page1"] != F["pages"] & F["pages"] > 1
		),
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.manage_theme,
		id='back_to_manage'
	),
	state=AdminMenuStates.manage_theme_questions,
	getter=getter_questions
)

manage_question = Window(
	Const('Редактирование вопроса\n'),
	Format(
		'Вопрос: <b>{question}</b>',
		when=F['question']
	),
	Format('Ответ: <b>{answer}</b>'),
	SwitchTo(
		text=Const('Изменить ответ'),
		id='change_answer',
		state=AdminMenuStates.change_answer
	),
	SwitchTo(
		text=Const('Изменить медиа'),
		id='change_media',
		state=AdminMenuStates.change_media
	),
	SwitchTo(
		text=Const('Изменить вопрос'),
		id='change_question',
		state=AdminMenuStates.change_question
	),
	SwitchTo(
		text=Const('Удалить вопрос'),
		id='delete_question',
		state=AdminMenuStates.delete_question_confirm
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.manage_theme_questions,
		id='back_to_manage'
	),
	state=AdminMenuStates.manage_question,
	getter=getter_question
)

delete_question_confirm = Window(
	Const('Удалить вопрос?'),
	Button(
		text=Const('Да, удалить'),
		id='delete_question',
		on_click=on_delete_question
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.manage_question,
		id='back_to_manage'
	),
	state=AdminMenuStates.delete_question_confirm
)

change_answer = Window(
	Const('Введите новый ответ'),
	MessageInput(
		func=on_change_answer,
		content_types=[ContentType.TEXT]
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.manage_question,
		id='back_to_manage'
	),
	state=AdminMenuStates.change_answer
)

change_question = Window(
	Const(
		'Отправьте новый вопрос\n\n<b>Можно отправить фото, видео, документ с описанием или просто текст.</b>'
	),
	MessageInput(
		func=on_change_question_text,
		content_types=[ContentType.TEXT]
	),
	MessageInput(
		func=on_change_question_media_and_text,
		content_types=[ContentType.PHOTO, ContentType.DOCUMENT, ContentType.VIDEO]
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.manage_question,
		id='back_to_manage'
	),
	state=AdminMenuStates.change_question
)

change_media = Window(
	Const('Отправьте новое медиа'),
	MessageInput(
		func=on_change_question_media,
		content_types=[ContentType.PHOTO, ContentType.DOCUMENT, ContentType.VIDEO]
	),
	SwitchTo(
		text=Const('Назад'),
		state=AdminMenuStates.manage_question,
		id='back_to_manage'
	),
	state=AdminMenuStates.change_media
)

create_new_question = Window(
	Const(
		'Отправьте новый вопрос\n\n<b>Можно отправить фото, видео, документ с описанием или просто текст.</b>'
	),
	MessageInput(
		func=on_create_question_text,
		content_types=[ContentType.TEXT]
	),
	MessageInput(
		func=on_create_question_media,
		content_types=[ContentType.PHOTO, ContentType.DOCUMENT, ContentType.VIDEO]
	),
	SwitchTo(
		text=Const('Отмена'),
		state=AdminMenuStates.manage_theme,
		id='back_to_manage'
	),
	state=AdminMenuStates.add_question
)

create_new_question_answer = Window(
	Const('Введите ответ на вопрос'),
	MessageInput(
		func=on_create_question_answer,
		content_types=[ContentType.TEXT]
	),
	SwitchTo(
		text=Const('Отмена'),
		state=AdminMenuStates.manage_theme,
		id='back_to_manage'
	),
	state=AdminMenuStates.add_question_answer
)

admin_dialog = Dialog(
	admin_menu,
	theme_select,
	theme_manage,
	delete_theme,
	questions,
	manage_question,
	delete_question_confirm,
	change_answer,
	change_question,
	change_media,
	create_new_question,
	create_new_question_answer
)

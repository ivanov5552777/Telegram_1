import os
import re
import sys

def patch_werygram_core():
    settings_path = "TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java"
    userconfig_path = "TMessagesProj/src/main/java/org/telegram/messenger/UserConfig.java"
    messages_path = "TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java"
    
    if not os.path.exists(settings_path):
        print(f"🚨 КРИТИЧЕСКАЯ ОШИБКА: Файл не найден: {settings_path}")
        sys.exit(1)

    print("⏳ Авто-патчер Werygram (Стиль двухстрочного свитча) запущен...")

    # ==========================================
    # 1. МОДЕРНИЗАЦИЯ ИНТЕРФЕЙСА (SettingsActivity)
    # ==========================================
    with open(settings_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Полная зачистка старых компонентов мода
    code = re.sub(r'case 9999:.*?break;', '', code, flags=re.DOTALL)
    code = re.sub(r'items\.add\(SettingCell\.Factory\.of\(9999,[\s\S]*?\);\s*', '', code)
    code = re.sub(r'items\.add\(UItem\.asCheck\(9999,[\s\S]*?\);\s*', '', code)
    code = re.sub(r'public static class WeryGramSettingsActivity[\s\S]*?$', '', code, flags=re.MULTILINE)
    code = re.sub(r'public static class WerygramSettingsActivity[\s\S]*?$', '', code, flags=re.MULTILINE)

    # Создаем нативную кнопку Werygram на главном экране настроек
    werygram_btn = 'items.add(SettingCell.Factory.of(9999, 0xFF55CA47, 0xFF27B434, R.drawable.msg_settings, "Werygram"));'

    # Вставляем её в самый верх первого списка категорий
    match_notif = re.search(r'(items\.add\([\s\S]*?[nN]otif[\s\S]*?\);)', code)
    if match_notif:
        anchor = match_notif.group(1)
        code = code.replace(anchor, f'{werygram_btn}\n        {anchor}')
        print("✅ Главная кнопка 'Werygram' установлена в список!")
    else:
        code = code.replace("switch (item.id) {", f"{werygram_btn}\n        switch (item.id) {{")

    # Обработчик нажатия для перехода на наш кастомный экран
    switch_anchor = "switch (item.id) {"
    if switch_anchor in code:
        click_logic = """case 9999: {
            presentFragment(new WerygramSettingsActivity());
            break;
        }"""
        code = code.replace(switch_anchor, f"{switch_anchor}\n            {click_logic}")
        print("✅ Обработчик клика привязан к новому экрану!")

    # Внедряем класс WerygramSettingsActivity со стилем один в один как на скрипте IMG_20260603_202806.jpg
    code = code.strip()
    if code.endswith("}"):
        werygram_menu_class = """
    public static class WerygramSettingsActivity extends org.telegram.ui.ActionBar.BaseFragment {
        @Override
        public android.view.View createView(android.content.Context context) {
            actionBar.setBackButtonImage(R.drawable.ic_ab_back);
            actionBar.setTitle("Werygram");
            actionBar.setActionBarMenuOnItemClick(new org.telegram.ui.ActionBar.ActionBar.ActionBarMenuOnItemClick() {
                @Override
                public void onItemClick(int id) {
                    if (id == -1) {
                        finishFragment();
                    }
                }
            });

            // Основной контейнер-скролл
            android.widget.ScrollView scrollView = new android.widget.ScrollView(context);
            scrollView.setFillViewport(true);
            scrollView.setBackgroundColor(org.telegram.ui.ActionBar.Theme.getColor(org.telegram.ui.ActionBar.Theme.key_windowBackgroundWhite));

            android.widget.LinearLayout linearLayout = new android.widget.LinearLayout(context);
            linearLayout.setOrientation(android.widget.LinearLayout.VERTICAL);
            scrollView.addView(linearLayout, new android.widget.FrameLayout.LayoutParams(android.widget.FrameLayout.LayoutParams.MATCH_PARENT, android.widget.FrameLayout.LayoutParams.WRAP_CONTENT));

            // Контейнер для кнопки (FrameLayout)
            android.widget.FrameLayout cell = new android.widget.FrameLayout(context);
            cell.setBackground(org.telegram.ui.ActionBar.Theme.getSelectorDrawable(true));
            int pLeft = org.telegram.messenger.AndroidUtilities.dp(16);
            int pTop = org.telegram.messenger.AndroidUtilities.dp(12);
            cell.setPadding(pLeft, pTop, pLeft, pTop);

            // Вертикальный лейаут для текстов (Слева)
            android.widget.LinearLayout textLayout = new android.widget.LinearLayout(context);
            textLayout.setOrientation(android.widget.LinearLayout.VERTICAL);

            // Главный заголовок
            android.widget.TextView titleView = new android.widget.TextView(context);
            titleView.setText("Telegram Premium");
            titleView.setTextSize(android.util.TypedValue.COMPLEX_UNIT_SP, 16);
            titleView.setTextColor(org.telegram.ui.ActionBar.Theme.getColor(org.telegram.ui.ActionBar.Theme.key_windowBackgroundWhiteBlackText));
            textLayout.addView(titleView, org.telegram.ui.Components.LayoutHelper.createLinear(org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT, org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT));

            // Описание под ним (как на картинке IMG_20260603_202806.jpg)
            android.widget.TextView subtitleView = new android.widget.TextView(context);
            subtitleView.setText("Выдает функции Telegram Premium визуально");
            subtitleView.setTextSize(android.util.TypedValue.COMPLEX_UNIT_SP, 13);
            subtitleView.setTextColor(org.telegram.ui.ActionBar.Theme.getColor(org.telegram.ui.ActionBar.Theme.key_windowBackgroundWhiteGrayText));
            textLayout.addView(subtitleView, org.telegram.ui.Components.LayoutHelper.createLinear(org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT, org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT, 0, 3, 0, 0));

            cell.addView(textLayout, org.telegram.ui.Components.LayoutHelper.createFrame(org.telegram.ui.Components.LayoutHelper.MATCH_PARENT, org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT, android.view.Gravity.LEFT | android.view.Gravity.CENTER_VERTICAL, 0, 0, 68, 0));

            // Вертикальная разделительная полоса перед свитчем
            android.view.View verticalDivider = new android.view.View(context);
            verticalDivider.setBackgroundColor(org.telegram.ui.ActionBar.Theme.getColor(org.telegram.ui.ActionBar.Theme.key_divider));
            cell.addView(verticalDivider, org.telegram.ui.Components.LayoutHelper.createFrame(1, 24, android.view.Gravity.RIGHT | android.view.Gravity.CENTER_VERTICAL, 0, 0, 46, 0));

            // Фирменный синий тумблер Телеграма (Справа)
            final org.telegram.ui.Components.Switch switchView = new org.telegram.ui.Components.Switch(context);
            boolean isEnabled = org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("visual_premium", false);
            switchView.setChecked(isEnabled, false);
            cell.addView(switchView, org.telegram.ui.Components.LayoutHelper.createFrame(org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT, org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT, android.view.Gravity.RIGHT | android.view.Gravity.CENTER_VERTICAL));

            // Обработка клика по ВСЕЙ строке
            cell.setOnClickListener(new android.view.View.OnClickListener() {
                @Override
                public void onClick(android.view.View v) {
                    boolean newState = !org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("visual_premium", false);
                    org.telegram.messenger.MessagesController.getGlobalMainSettings().edit().putBoolean("visual_premium", newState).apply();
                    switchView.setChecked(newState, true); // Переключаем с плавной анимацией
                    
                    android.widget.Toast.makeText(getParentActivity(), newState ? "WeryGram: Visual Premium АКТИВИРОВАН! 🎉" : "WeryGram: Visual Premium ОТКЛЮЧЕН", android.widget.Toast.LENGTH_SHORT).show();
                    org.telegram.messenger.UserConfig.getInstance(currentAccount).getCurrentUser();
                }
            });

            linearLayout.addView(cell, org.telegram.ui.Components.LayoutHelper.createLinear(org.telegram.ui.Components.LayoutHelper.MATCH_PARENT, org.telegram.ui.Components.LayoutHelper.WRAP_CONTENT));

            // Тонкая горизонтальная линия-разделитель под ячейкой
            android.view.View bottomDivider = new android.view.View(context);
            bottomDivider.setBackgroundColor(org.telegram.ui.ActionBar.Theme.getColor(org.telegram.ui.ActionBar.Theme.key_divider));
            linearLayout.addView(bottomDivider, org.telegram.ui.Components.LayoutHelper.createLinear(org.telegram.ui.Components.LayoutHelper.MATCH_PARENT, 1));

            fragmentView = scrollView;
            return fragmentView;
        }
    }
"""
        code = code[:-1] + werygram_menu_class + "\n}"
        print("✅ Нативный двухстрочный дизайн кнопки успешно добавлен в код!")

    with open(settings_path, "w", encoding="utf-8") as f:
        f.write(code)

    # ==========================================
    # 2. АКТИВАЦИЯ ПРЕМИУМА В СИСТЕМЕ (UserConfig)
    # ==========================================
    if os.path.exists(userconfig_path):
        with open(userconfig_path, "r", encoding="utf-8") as f:
            uc_code = f.read()
        
        uc_code = re.sub(r'// WG_START.*?// WG_END', '', uc_code, flags=re.DOTALL)
        
        uc_anchor = "public TLRPC.User getCurrentUser() {"
        if uc_anchor in uc_code:
            uc_injection = """public TLRPC.User getCurrentUser() {
        // WG_START
        if (currentUser != null && org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("visual_premium", false)) {
            currentUser.premium = true;
            currentUser.verified = true;
        }
        // WG_END"""
            uc_code = uc_code.replace(uc_anchor, uc_injection)
            with open(userconfig_path, "w", encoding="utf-8") as f:
                f.write(uc_code)
            print("✅ Системная логика Premium добавлена в UserConfig!")

    # ==========================================
    # 3. ПОДМЕНА СТАТУСА ДЛЯ ОТОБРАЖЕНИЯ (MessagesController)
    # ==========================================
    if os.path.exists(messages_path):
        with open(messages_path, "r", encoding="utf-8") as f:
            mc_code = f.read()
        
        mc_code = re.sub(r'// WG_MC_START.*?// WG_MC_END', '', mc_code, flags=re.DOTALL)
        
        mc_code = re.sub(
            r'public TLRPC\.User getUser\((Long|Integer)\s+(\w+)\)\s*\{\s*return\s+(\w+)\.get\(\2\);\s*\}',
            r'''public TLRPC.User getUser(\1 \2) {
        TLRPC.User user = \3.get(\2);
        // WG_MC_START
        if (user != null && \2 != null && \2.equals(UserConfig.getInstance(currentAccount).getClientUserId())) {
            if (org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("visual_premium", false)) {
                user.premium = true;
                user.verified = true;
            }
        }
        // WG_MC_END
        return user;
    }''',
            mc_code
        )
        with open(messages_path, "w", encoding="utf-8") as f:
            f.write(mc_code)
        print("✅ Глобальный перехватчик ID обновлен!")

    print("\n🎉 ВСЁ СМОДЕЛИРОВАНО ИДЕАЛЬНО! Отправляем на компиляцию.")

if __name__ == "__main__":
    patch_werygram_core()

#!/usr/bin/env python3
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "TMessagesProj", "src", "main", "java")

def find_file(name):
    for dp, _, files in os.walk(SRC):
        if name in files:
            return os.path.join(dp, name)
    return None

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def write(p, t):
    with open(p, "w", encoding="utf-8") as f: f.write(t)
    print(f"✔ {os.path.relpath(p, ROOT)}")

def patch_once(path, marker, insertion, before=False):
    text = read(path)
    if insertion.strip() in text:
        print(f"↩ skip {os.path.relpath(path, ROOT)}"); return True
    if marker not in text:
        print(f"✘ MARKER NOT FOUND: {marker!r}", file=sys.stderr); return False
    repl = (insertion + "\n" + marker) if before else (marker + "\n" + insertion)
    write(path, text.replace(marker, repl, 1)); return True

ACTIVITY = '''\
package org.telegram.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.widget.LinearLayout;
import org.telegram.messenger.MessagesController;
import org.telegram.messenger.UserConfig;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.Cells.TextCheckCell;

public class WeryGramPremiumActivity extends BaseFragment {
    @Override
    public android.view.View createView(Context context) {
        actionBar.setBackButtonImage(org.telegram.messenger.R.drawable.ic_ab_back);
        actionBar.setTitle("WeryGram");
        actionBar.setActionBarMenuOnItemClick(new org.telegram.ui.ActionBar.ActionBar.ActionBarMenuOnItemClick() {
            @Override public void onItemClick(int id) { if (id == -1) finishFragment(); }
        });

        LinearLayout root = new LinearLayout(context);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundWhite));

        TextCheckCell premiumCell = new TextCheckCell(context);
        SharedPreferences prefs = MessagesController.getGlobalMainSettings();
        boolean isEnabled = prefs.getBoolean("wery_visual_premium", false);

        premiumCell.setTextAndValueAndCheck(
            "Visual Premium", 
            "Дает визуально телеграм премиум", 
            isEnabled, 
            false, 
            true
        );

        premiumCell.setOnClickListener(v -> {
            boolean newState = !prefs.getBoolean("wery_visual_premium", false);
            prefs.edit().putBoolean("wery_visual_premium", newState).apply();
            premiumCell.setChecked(newState);
            
            // Включаем визуал премиума в самом приложении
            UserConfig.getInstance(currentAccount).isPremium = newState;
            UserConfig.getInstance(currentAccount).saveConfig(false);
        });

        root.addView(premiumCell);
        fragmentView = root;
        return fragmentView;
    }
}
'''

def main():
    print("▶ WeryGram patcher\n")
    errors = 0

    sa = find_file("SettingsActivity.java")
    if not sa: print("✘ SettingsActivity.java not found", file=sys.stderr); sys.exit(1)

    if not patch_once(sa, "import org.telegram.ui.Components.", "import org.telegram.ui.WeryGramPremiumActivity;", before=True): errors += 1

    fill_anchors = [
        "void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {",
        "public void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {",
        "private void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {",
    ]
    fill_anchor = next((a for a in fill_anchors if a in read(sa)), None)
    if fill_anchor:
        # ИСПРАВЛЕНИЕ ЗДЕСЬ: добавлен полный путь org.telegram.messenger.R.drawable
        if not patch_once(sa, fill_anchor,
            fill_anchor.replace("{", "{\n        items.add(0, UItem.asButton(1000, org.telegram.messenger.R.drawable.msg_settings, \"WeryGram\"));")):
            errors += 1
        
        click_anchors = [
            "void onItemClick(UItem item, View view, int position, float x, float y) {",
            "public void onItemClick(UItem item, View view, int position, float x, float y) {",
            "private void onItemClick(UItem item, View view, int position, float x, float y) {",
            "void onClick(UItem item, View view, int position, float x, float y) {",
            "public void onClick(UItem item, View view, int position, float x, float y) {",
            "void onClick(UItem item) {",
            "public void onClick(UItem item) {",
            "onItemClick = (item) -> {",
            "onItemClick = item -> {",
        ]
        click_anchor = next((a for a in click_anchors if a in read(sa)), None)
        if click_anchor:
            if not patch_once(sa, click_anchor,
                click_anchor.replace("{", "{\n        if (item != null && item.id == 1000) { presentFragment(new WeryGramPremiumActivity()); return; }")):
                errors += 1
        else:
            print("✘ SettingsActivity: onItemClick не найден", file=sys.stderr); errors += 1
    else:
        print("✘ SettingsActivity: fillItems не найден", file=sys.stderr); errors += 1

    dest = os.path.join(os.path.dirname(sa), "WeryGramPremiumActivity.java")
    if os.path.exists(dest):
        os.remove(dest)
    with open(dest, "w", encoding="utf-8") as f: f.write(ACTIVITY)
    print("✔ created WeryGramPremiumActivity.java")

    if errors > 0:
        print(f"\n✘ {errors} ошибок — сборка остановлена", file=sys.stderr)
        sys.exit(1)
    print("\n✅ Done.")

if __name__ == "__main__":
    main()
    

package org.telegram.ui;

import android.content.Context;
import android.view.View;
import android.widget.FrameLayout;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.Theme;

public class WeryGramActivity extends BaseFragment {

    @Override
    public View createView(Context context) {
        // Настраиваем верхнюю панель (шапку экрана)
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setTitle("WeryGram Settings");
        actionBar.setAllowOverlayTitle(true);
        
        // Настраиваем действие для стрелочки "Назад"
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment(); // Закрыть этот экран и вернуться назад
                }
            }
        });

        // Создаем контейнер фона, который автоматически меняет цвет (светлый/темный)
        fragmentView = new FrameLayout(context);
        fragmentView.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundWhite));

        return fragmentView;
    }
}

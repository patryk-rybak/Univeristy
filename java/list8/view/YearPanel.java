package view;

import javax.swing.*;
import java.awt.*;
import java.util.Calendar;
import java.util.GregorianCalendar;

public class YearPanel extends JPanel {

	private String[] monthNames;
	Font font;

	public YearPanel() {
		monthNames = new String[]{"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
		font = new Font("Arial", Font.PLAIN, 50);

		setLayout(new GridLayout(3, 4, 10, 10));

		for (int month = 1; month <= 12; month++) {
			JPanel monthPanel = new JPanel(new BorderLayout());
			JLabel temp = new JLabel(monthNames[month - 1], SwingConstants.CENTER);
			temp.setFont(font);
			monthPanel.add(temp, BorderLayout.CENTER);
			monthPanel.setBackground(Color.LIGHT_GRAY);
			add(monthPanel);
		}
	}

	public JPanel getMonthPanel(int i) {
		return (JPanel)getComponent(i);
	}
}

package view;

import java.util.Calendar;
import javax.swing.*;
import java.awt.*;
import model.*;

public class ToolBarPanel extends JPanel {

	JButton prevMonthButton, nextMonthButton;
	JSpinner yearSpinner;
	JSlider monthSlider;
	JLabel monthLabel;
	Font font;

	public ToolBarPanel() {
		setLayout(new FlowLayout());
		font = new Font("Arial", Font.PLAIN, 30);

		JLabel temp2 = new JLabel("Month :");
		temp2.setFont(font);
		add(temp2);

		prevMonthButton = new JButton("<-");
		prevMonthButton.setFont(font);
		add(prevMonthButton);

		monthSlider = new JSlider(JSlider.HORIZONTAL, 0, 11, Calendar.getInstance().get(Calendar.MONTH));
		add(monthSlider);

		nextMonthButton = new JButton("->");
		nextMonthButton.setFont(font);
		add(nextMonthButton);
		add(new JLabel("            "));

		JLabel temp1 = new JLabel("Year :");
		temp1.setFont(font);
		add(temp1);

		yearSpinner = new JSpinner(new SpinnerNumberModel(Calendar.getInstance().get(Calendar.YEAR), 1, 9999, 1));
		yearSpinner.setEditor(new JSpinner.NumberEditor(yearSpinner, "#"));
		yearSpinner.setFont(font);
		add(yearSpinner);
	}

	public void refresh(CalendarModel model) {
		yearSpinner.setValue(model.getYear());
		monthSlider.setValue(model.getMonth());
	}

	public JButton getPrevMonthButton() {
		return prevMonthButton;
	}

	public JButton getNextMonthButton() {
		return nextMonthButton;
	}

	public JSpinner getYearSpinner() {
		return yearSpinner;
	}

	public JSlider getMonthSlider() {
		return monthSlider;
	}
}

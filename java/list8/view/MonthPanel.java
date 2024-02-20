package view;

import javax.swing.*;
import java.awt.*;
import model.*;

public class MonthPanel extends JPanel {

	JList<String> currMonthList;
	JList<String> prevMonthList;
	JList<String> nextMonthList;
	DefaultListModel<String> prevMonthModel;
	DefaultListModel<String> currMonthModel;
	DefaultListModel<String> nextMonthModel;
	JPanel headerPanel;
	JLabel l1;
	JLabel l2;
	JLabel l3;
	String[] monthNames;
	Font font1;
	Font font2;

	public MonthPanel() {
		monthNames = new String[]{"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};

		setLayout(new BorderLayout());

		headerPanel = new JPanel(new GridLayout(0,3));
		l1 = new JLabel();
		l2 = new JLabel();
		l3 = new JLabel();
		headerPanel.add(l1);
		headerPanel.add(l2);
		headerPanel.add(l3);

		currMonthModel = new DefaultListModel<>();
		prevMonthModel = new DefaultListModel<>();
		nextMonthModel = new DefaultListModel<>();
		currMonthList = new JList<>(currMonthModel);
		prevMonthList = new JList<>(prevMonthModel);
		nextMonthList = new JList<>(nextMonthModel);

		font1 = new Font("Arial", Font.PLAIN, 25);
		font2 = new Font("Arial", Font.PLAIN, 30);
		currMonthList.setFont(font1);
		prevMonthList.setFont(font1);
		nextMonthList.setFont(font1);
		l1.setFont(font2);
		l2.setFont(font2);
		l3.setFont(font2);

		DefaultListCellRenderer renderer = new DefaultListCellRenderer() {
			@Override
			public Component getListCellRendererComponent(
					JList list, Object value,
					int index, boolean isSelected,
					boolean cellHasFocus)
			{
				super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);

				String dayValue = (String) value;
				if (dayValue.contains("Sunday")) {
					setForeground(Color.RED);
				} else {
					setForeground(Color.BLACK);
				}
				setHorizontalAlignment(SwingConstants.LEFT);
				return this;
			}
		};

		currMonthList.setCellRenderer(renderer);
		prevMonthList.setCellRenderer(renderer);
		nextMonthList.setCellRenderer(renderer);

		JPanel temp = new JPanel(new GridLayout(0, 3));

		add(headerPanel, BorderLayout.NORTH);

		temp.add(new JScrollPane(prevMonthList)/* , BorderLayout.CENTER */);
		temp.add(new JScrollPane(currMonthList));
		temp.add(new JScrollPane(nextMonthList));

		add(temp, BorderLayout.CENTER);

	}

	public void setHeaderLabels(int currMonth) {
		l1.setText(monthNames[(currMonth == 0) ? 11 : currMonth - 1]);
		l2.setText(monthNames[currMonth]);
		l3.setText(monthNames[(currMonth == 11) ? 0 : currMonth + 1]);
	}

	public void changeHeaderLabels(CalendarModel model) {
		l1.setText(monthNames[(model.getMonth() == 0) ? 11 : model.getMonth() - 1]);
		l2.setText(monthNames[model.getMonth()]);
		l3.setText(monthNames[(model.getMonth() == 11) ? 0 : model.getMonth() + 1]);
	}

	public void setListModel(String[] prev, String[] curr, String[] next) {
		prevMonthModel.clear();
		currMonthModel.clear();
		nextMonthModel.clear();
		for (String record : prev) { prevMonthModel.addElement(record); }
		for (String record : curr) { currMonthModel.addElement(record); }
		for (String record : next) { nextMonthModel.addElement(record); }
	}
}


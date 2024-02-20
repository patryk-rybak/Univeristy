package view;

import javax.swing.*;
import java.awt.*;
import model.*;
import java.util.Calendar;

public class MainPanel extends JPanel {
	JTabbedPane tabPane;
	YearPanel page1;
	MonthPanel page2;
	ToolBarPanel toolBar;
	Calendar calendar;
	int currYear;
	int currMonth;
	private String[] monthNames;
	Font font;

	public MainPanel() {
		setLayout(new BorderLayout());

		font = new Font("Arial", Font.PLAIN, 25);
		monthNames = new String[]{"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};

		calendar = Calendar.getInstance();
		currYear = calendar.get(Calendar.YEAR);
		currMonth = calendar.get(Calendar.MONTH);

		tabPane = new JTabbedPane();
		tabPane.setFont(font);
		page1 = new YearPanel();
		page2 = new MonthPanel();
		page2.setHeaderLabels(currMonth);

		tabPane.addTab(String.valueOf(currYear), page1);
		tabPane.addTab(monthNames[currMonth], page2);
		add(tabPane, BorderLayout.CENTER);

		toolBar = new ToolBarPanel();
		add(toolBar, BorderLayout.SOUTH);
	}

	public void refresh(CalendarModel model){
		toolBar.refresh(model);
		tabPane.setTitleAt(0, String.valueOf(model.getYear()));
		tabPane.setTitleAt(1, monthNames[model.getMonth()]);
		page2.changeHeaderLabels(model);
	}

	public ToolBarPanel getToolBarPanel() {
		return toolBar;
	}

	public YearPanel getYearPanel() {
		return page1;
	}

	public MonthPanel getMonthPanel() {
		return page2;
	}	

	public JTabbedPane getTabbedPane() {
		return tabPane; 
	}

	public void setTabPanIndex(int index) {
		tabPane.setSelectedIndex(index);
	}



}

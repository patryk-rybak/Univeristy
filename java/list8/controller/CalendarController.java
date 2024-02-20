package controller;

import javax.swing.*;
import java.awt.*;
import controller.*;
import model.*;
import view.*;
import javax.swing.event.*;
import java.awt.event.*;

public class CalendarController {

	CalendarModel model;
	MainPanel view;

	public CalendarController(CalendarModel model, MainPanel view) {
		this.model = model;
		this.view = view;

		view.getToolBarPanel().getPrevMonthButton().addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				model.changeMonth(-1);
				view.refresh(model);
				buildCalendar();
			}
		});

		view.getToolBarPanel().getNextMonthButton().addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				model.changeMonth(1);
				view.refresh(model);
				buildCalendar();
			}
		});

		view.getToolBarPanel().getYearSpinner().addChangeListener(new ChangeListener() {
			@Override
			public void stateChanged(ChangeEvent e) {
				model.setYear((Integer) view.getToolBarPanel().getYearSpinner().getValue());
				view.refresh(model);
				buildCalendar();
			}
		});

		view.getToolBarPanel().getMonthSlider().addChangeListener(new ChangeListener() {
			@Override
			public void stateChanged(ChangeEvent e) {
				JSlider source = (JSlider) e.getSource();
				if (!source.getValueIsAdjusting()) {
					model.setMonth((Integer) source.getValue());
					view.refresh(model);
					buildCalendar();
				}
			}
		});
		view.getTabbedPane().addChangeListener(new ChangeListener() {
			@Override
			public void stateChanged(ChangeEvent e) {
				buildCalendar();
			}
		});

		for (int i = 0; i < 12; i++) {
			int idx = i;
			view.getYearPanel().getMonthPanel(i).addMouseListener(new MouseAdapter() {		
				@Override
				public void mouseClicked(MouseEvent evt) {
					model.setMonth(idx);
					view.getToolBarPanel().refresh(model);
					view.refresh(model);
					view.setTabPanIndex(1);
					buildCalendar();
				}
				@Override
				public void mouseEntered(MouseEvent e) {
					JPanel hoveredMonth = (JPanel) e.getComponent();
					hoveredMonth.setBackground(Color.CYAN);
				}
				@Override
				public void mouseExited(MouseEvent e) {
					JPanel exitedMonth = (JPanel) e.getComponent();
					exitedMonth.setBackground(Color.LIGHT_GRAY);
				}
			});
		}
	}

	public void buildCalendar() {
		JTabbedPane temp = view.getTabbedPane();
		if (temp.getSelectedIndex() == 1) {
			view.getToolBarPanel().getMonthSlider().setValue(model.getMonth());
			view.getToolBarPanel().getYearSpinner().setValue(model.getYear());
			String[] prevMonth = model.getPrevMonth();
			String[] currMonth = model.getCurrMonth();
			String[] nextMonth = model.getNextMonth();
			view.getMonthPanel().setListModel(prevMonth, currMonth, nextMonth);
		}
	}
	


}

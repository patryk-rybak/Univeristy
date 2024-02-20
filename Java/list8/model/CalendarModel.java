package model;

import java.util.Calendar;
import java.util.GregorianCalendar;
import javax.swing.*;

public class CalendarModel extends AbstractListModel {

	GregorianCalendar calendar;
	private String[] dayNames;
	private String[] monthNames;

	public CalendarModel() {
		calendar = new GregorianCalendar();
		dayNames = new String[]{"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
		monthNames = new String[]{"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
	}

	@Override
	public int getSize() {
		int res = calendar.getActualMaximum(Calendar.DAY_OF_MONTH);
		return res;
	}

	@Override
	public String getElementAt(int index) {
		GregorianCalendar temp = (GregorianCalendar) calendar.clone();
		temp.set(Calendar.DAY_OF_MONTH, index + 1);
		int dayOfWeek = temp.get(Calendar.DAY_OF_WEEK);
		int monthOfYear = temp.get(Calendar.YEAR);
		return dayNames[dayOfWeek - 1] + ", " + String.valueOf(index + 1) + ", " + monthNames[monthOfYear - 1];
	}

	public void setMonth(int month) {
		calendar.set(Calendar.MONTH, month);
		fireContentsChanged(this, 0, getSize() - 1);
	}

	public void setYear(int year) {
		calendar.set(Calendar.YEAR, year);
		fireContentsChanged(this, 0, getSize() - 1);
	}

	public void changeMonth(int i) {
		calendar.add(Calendar.MONTH, i);
		fireContentsChanged(this, 0, getSize() - 1);
	}

	public void changeYear(int i) {
		calendar.add(Calendar.YEAR, i);
		fireContentsChanged(this, 0, getSize() - 1);
	}

	public int getMonth() {
		return calendar.get(Calendar.MONTH);
	}

	public int getYear() {
		return calendar.get(Calendar.YEAR);
	}

	public String[] getCurrMonth() {
		GregorianCalendar temp = (GregorianCalendar) calendar.clone();

		int numberOfDays = temp.getActualMaximum(Calendar.DAY_OF_MONTH);
		String[] currMonthRecords = new String[numberOfDays];
		int year = temp.get(Calendar.YEAR);
		int month = temp.get(Calendar.MONTH) + 1;
		for(int i = 0; i < numberOfDays; i++) {
			temp.set(Calendar.DAY_OF_MONTH, i + 1);
			if (year == 1582 && i >= 4 && i < 14 && month == 10) {
				currMonthRecords[i] = "";
				continue; }
			currMonthRecords[i] = String.valueOf(i + 1) + " " + dayNames[temp.get(Calendar.DAY_OF_WEEK) - 1];
		}
		return currMonthRecords;
	}

	public String[] getPrevMonth() {
		GregorianCalendar temp = (GregorianCalendar) calendar.clone();

		temp.add(Calendar.MONTH, -1);
		int numberOfDays = temp.getActualMaximum(Calendar.DAY_OF_MONTH);
		String[] prevMonthRecords = new String[numberOfDays];
		int year = temp.get(Calendar.YEAR);
		int month = temp.get(Calendar.MONTH) + 1;
		for(int i = 0; i < numberOfDays; i++) {
			temp.set(Calendar.DAY_OF_MONTH, i + 1);
			if (year == 1582 && i >= 4 && i < 14 && month == 10) { 
				prevMonthRecords[i] = "";
				continue; }
			prevMonthRecords[i] = String.valueOf(i + 1) + " " + dayNames[temp.get(Calendar.DAY_OF_WEEK) - 1];
		}
		return prevMonthRecords;
	}

	public String[] getNextMonth() {
		GregorianCalendar temp = (GregorianCalendar) calendar.clone();

		temp.add(Calendar.MONTH, 1);
		int numberOfDays = temp.getActualMaximum(Calendar.DAY_OF_MONTH);
		String[] nextMonthRecords = new String[numberOfDays];
		int year = temp.get(Calendar.YEAR);
		int month = temp.get(Calendar.MONTH) + 1;
		for(int i = 0; i < numberOfDays; i++) {
			temp.set(Calendar.DAY_OF_MONTH, i + 1);
			if (year == 1582 && i >= 4 && i < 14 && month == 10) {
				nextMonthRecords[i] = "";
				continue; }
			nextMonthRecords[i] = String.valueOf(i + 1) + " " + dayNames[temp.get(Calendar.DAY_OF_WEEK) - 1];
		}
		return nextMonthRecords;
	}
}

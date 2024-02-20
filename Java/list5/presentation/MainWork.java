package presentation;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

class MainWork implements ActionListener {
	
	private Gui gui;

	public MainWork() {
		gui = new Gui(this);
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		String cmd = e.getActionCommand();
		System.out.println(cmd);
		switch (cmd) {
			case "submit" -> doSubmit(e);
			case "start" -> doStart(e);
			case "stop" -> doStop(e);
			case "exit" -> doExit(e);
			case "range" -> doRange(e);
			case "attempts" -> doAttempts(e);
		}
	}

	void doSubmit(ActionEvent e) { System.out.println("dupa"); }
	void doStart(ActionEvent e) { System.out.println("chuj"); }
	void doStop(ActionEvent e) { System.out.println("chuj"); }
	void doExit(ActionEvent e) { System.out.println("chuj"); }
	void doRange(ActionEvent e) { System.out.println("chuj"); }
	void doAttempts(ActionEvent e) { System.out.println("chuj"); }

	public static void main(String[] args) { new MainWork(); }
}

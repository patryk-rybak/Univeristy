import javax.swing.*;
import model.*;
import view.*;
import controller.*;

public class Main {
	
	public static void main(String[] args) {

		CalendarModel model = new CalendarModel();
		MainPanel view = new MainPanel();
		CalendarController controller = new CalendarController(model, view);


		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				JFrame window = new JFrame();
				window.setTitle("Calendar");
				window.add(view);
				window.setSize(1500, 1000);
				window.setLocationRelativeTo(null);
				window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				window.setVisible(true);
			}		
		});
	}
}

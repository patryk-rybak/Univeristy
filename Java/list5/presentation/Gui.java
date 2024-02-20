package presentation;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import static java.awt.Color.*;

class Gui extends JFrame {

	Gui(ActionListener a) {

		setLayout(new GridLayout(0,1));

		addTextFields(new String[]{"Numerator", "Denominator"});

		addScrollBar("range", 5, 20, a);

		addScrollBar("attempts", 1, 20, a); // niewidzianlny na poczatku
		
		addButtonsPanel(new String[]{ "submit", "start", "stop", "exit" }, a);

		setDefaultCloseOperation(DISPOSE_ON_CLOSE);
		pack();
		setLocationRelativeTo(null);
		setVisible(true);
	}


	private void addButtonsPanel(String[] cmd, ActionListener a) {
		// Panel sterujący
		JPanel pcon = new JPanel(new FlowLayout(FlowLayout.CENTER));
		pcon.setBorder(BorderFactory.createLineBorder(BLUE));
		for (int i = 0; i < cmd.length; i++) {
			JButton b = new JButton(cmd[i]);
			b.addActionListener(a);
			pcon.add(b);
		}
		add(pcon,"South");
	}

	private void addTextFields(String[] labels) {

		JPanel panel = new JPanel(new GridLayout(0, 2));
		for (int i = 0; i < labels.length; i++) {
			JLabel l = new JLabel(labels[i]);
			panel.add(l);
			JTextField textField = new JTextField(10);
			l.setLabelFor(textField);
			panel.add(textField);
		}
		add(panel);
	}

	private void addScrollBar(String name, int min, int max, ActionListener a) {
		assert min < max : "max should be greater than min";
			
		JPanel p = new JPanel(new GridLayout(0, 1));
		JScrollBar scrollBar = new JScrollBar(JScrollBar.HORIZONTAL);
		scrollBar.setName(name);
		scrollBar.setMinimum(min);
		scrollBar.setMaximum(max);
		scrollBar.setValue(min);

		JLabel valueLabel = new JLabel("Value: " + scrollBar.getValue());
        	valueLabel.setHorizontalAlignment(JLabel.CENTER);
		scrollBar.add(valueLabel);

		/* scrollBar.addAdjustmentListener(new AdjustmentListener() {
			@Override
			public void adjustmentValueChanged(AdjustmentEvent e) {
				ActionEvent event = new ActionEvent(this, ActionEvent.ACTION_PERFORMED, name);
				a.actionPerformed(event);
			}
		}); */
		scrollBar.addAdjustmentListener(new AdjustmentListener() {
			@Override
			public void adjustmentValueChanged(AdjustmentEvent e) {
				valueLabel.setText("Value: " + scrollBar.getValue());
			}
		});

		p.add(scrollBar);

		add(p);
	}
}


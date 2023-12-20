package gui;

import algorithms.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class Main extends JFrame {

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				new Main().setVisible(true);
			}
		});
	}

	private BST<String> bst;
	private DrawPanel drawPanel;

	public Main() {
		bst = new algorithms.BST<>();
		drawPanel = new DrawPanel();

		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setTitle("BST Dictionary");
		setSize(1500, 600);

		setupUI();

	}

	private void setupUI() {

		JPanel controlPanel = new JPanel();
		JButton insertButton = new JButton("Insert");
		JButton removeButton = new JButton("Remove");
		JButton searchButton = new JButton("Search");
		JButton clearButton = new JButton("Clear");
		JButton minButton = new JButton("Min");
		JButton maxButton = new JButton("Max");

		JTextField inputField = new JTextField(20);

		UIManager.put("OptionPane.messageFont", new Font("Arial", Font.PLAIN, 25));
		UIManager.put("OptionPane.minimumSize", new Dimension(500, 150));

		insertButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String value = inputField.getText();
				if (!value.isEmpty()) {
					if (!bst.insert(value)) {
						JOptionPane.showMessageDialog(Main.this,
								"There is already such thing as " + value);
						inputField.setText("");
						return;
					}
					drawPanel.repaint();
					inputField.setText("");
				}
			}
		});

		removeButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String value = inputField.getText();
				if (!value.isEmpty()) {
					if (!bst.remove(value)) {
						JOptionPane.showMessageDialog(Main.this,
								"There is no such thing as " + value);
						inputField.setText("");
						return;
					}

					drawPanel.repaint();
					inputField.setText("");
				}
			}
		});

		searchButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String value = inputField.getText();
				if (!value.isEmpty()) {
					boolean result = bst.search(value);
					JOptionPane.showMessageDialog(Main.this,
							"Search result for " + value + ": " + result);
					inputField.setText("");
				}
			}
		});

		clearButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				bst.clear();
				drawPanel.repaint();
			}
		});

		minButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String result = bst.min();
				JOptionPane.showMessageDialog(Main.this,
						"Result: " + result);
			}
		});

		maxButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String result = bst.max();
				JOptionPane.showMessageDialog(Main.this,
						"Result: " + result);
			}
		});

		controlPanel.add(new JLabel("Enter value: "));
		controlPanel.add(inputField);
		controlPanel.add(insertButton);
		controlPanel.add(removeButton);
		controlPanel.add(searchButton);
		controlPanel.add(clearButton);
		controlPanel.add(minButton);
		controlPanel.add(maxButton);
		
		Font largerFont = new Font("Arial", Font.PLAIN, 25);

		for (Component component : controlPanel.getComponents()) {
			if (component instanceof JComponent) {
				((JComponent) component).setFont(largerFont);
			}
		}

		Container container = getContentPane();
		container.setLayout(new BorderLayout());
		container.add(controlPanel, BorderLayout.NORTH);
		container.add(drawPanel, BorderLayout.CENTER);

	}

	private class DrawPanel extends JPanel {
		@Override
		protected void paintComponent(Graphics g) {
			super.paintComponent(g);
			drawTree(g, getWidth() / 2, 100, 1, bst.getRoot());
		}

		private void drawTree(Graphics g, int x, int y, int level, BST<String>.Node node) {
			if (node != null) {
				int diameter = 100;

				g.drawOval(x - diameter / 2, y - diameter / 2, diameter, diameter);

				Font originalFont = g.getFont();
				Font largerFont = originalFont.deriveFont(30f);
				g.setFont(largerFont);

				FontMetrics fontMetrics = g.getFontMetrics();
				String nodeValue = node.getValue().toString();
				int stringWidth = fontMetrics.stringWidth(nodeValue);
				int stringHeight = fontMetrics.getHeight();

				g.drawString(nodeValue, x - stringWidth / 2, y + stringHeight / 2);

				g.setFont(originalFont);

				if (node.getLeft() != null) {
					g.drawLine(x, y + diameter / 2, x - 600/level, y + 200 - diameter / 2);
					drawTree(g, x - 600/level, y + 200, level + 1, node.getLeft());
				}
				if (node.getRight() != null) {
					g.drawLine(x, y + diameter / 2, x + 600/level, y + 200 - diameter / 2);
					drawTree(g, x + 600/level, y + 200, level + 1, node.getRight());
				}
			}
		}
	}


}


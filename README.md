Diff Anywhere 1.0
=============

Description
-----------

**Diff Anywhere** is a cross-platform graphical application that allows users to compare two blocks of code or text. With a modern and user-friendly interface, you can easily paste code into two side-by-side text areas, and the application will display the differences in a bottom pane, highlighting the exact changes for easy identification.

Features
--------

*   **Cross-Platform Support**: Works seamlessly on Linux, macOS, and Windows.
    
*   **Side-by-Side Comparison**: Paste and compare code or text in two adjacent panes with line numbers.
    
*   **Highlighted Differences**: Exact differences within lines are highlighted for clarity.
    
*   **Modern UI**: A clean and modern interface with customizable colors for better readability.
    

Requirements
------------

*   **Python 3.x**
    
*   **Tkinter**: Standard Python GUI toolkit (usually included with Python installations).
    
*   **Difflib Module**: Comes standard with Python's standard library.
    

Installation
------------

1.  git clone https://github.com/yodabytz/diffanywhere.git
    
2.  cd diff-anywhere
    
3.  python diff\_anywhere.py
    

Usage
-----

1.  Run the diffany.py script using Python 3.
    
2.  **Paste Code/Text**
    
    *   Paste the first block of code into the left text area labeled **"Paste Code 1"**.
        
    *   Paste the second block of code into the right text area labeled **"Paste Code 2"**.
        
3.  **View Differences**
    
    *   The differences will automatically appear in the bottom pane labeled **"Differences"**.
        
    *   Differences are highlighted, and exact changes within lines are marked with a gold background and black text for visibility.
        

Platforms
---------

*   **Linux**
    
*   **macOS**
    
*   **Windows**
    

Needed Libraries
----------------

*   **Tkinter**
    
    *   Usually included with Python.
        
    *   bash Copy code# For Debian/Ubuntusudo apt-get install python3-tk# For macOS using Homebrewbrew install python-tk# For Windows# Tkinter comes with the standard Python installer from python.org
        
*   **Difflib**
    
    *   Comes with Python's standard library; no installation required.
        

Screenshot
-----------

<img src="https://raw.githubusercontent.com/yodabytz/diffanywhere/refs/heads/main/diffanywhere.png?raw=true" width="600">

Contributing
------------

Contributions are welcome! Please follow these steps:

1.  Click the **Fork** button at the top-right corner of the repository page.
    
2.  git checkout -b feature/YourFeatureName
    
3.  git commit -am 'Add a feature'
    
4.  git push origin feature/YourFeatureName
    
5.  Submit your pull request for review.
    

License
-------

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

Acknowledgements
----------------

*   **Python**: Programming language used.
    
*   **Tkinter**: For the GUI components.
    
*   **Difflib**: For computing text differences.

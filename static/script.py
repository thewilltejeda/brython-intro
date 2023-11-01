# Importing required functionalities from the Brython's browser module
from browser import document, timer


# Initialize a dictionary to hold the state of the application
state = {
    "timerRunning": False,  # Indicates if the timer is currently running
    "timerValue": 0,        # Holds the current value of the timer in seconds
    "interval": None        # Will store the reference to the timer interval
}


# Accessing the HTML DOM elements using the browser's document object
timerElement = document["timer"]  # Get reference to the timer display element
circleContainer = document.select_one('.circle-container')  # Get the main circle container using CSS selector
contentDiv = document.select_one('.content')  # Get the content div inside the circle
timerInputSection = document["timerInputSection"]  # Get the input section where users set the timer value


# Function to format time in a readable manner, converting seconds to hours, minutes, and seconds format
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
    

# Function to update the timer value based on user input
def setTimerValue(event=None):
    inputValue = int(document["timerInput"].value)  # Access and convert the timer input value to integer
    timeUnit = document["timeUnit"].value  # Access the selected time unit (seconds, minutes, hours)

    # Convert input to seconds based on chosen time unit
    if timeUnit == "minutes":
        inputValue *= 60
    elif timeUnit == "hours":
        inputValue *= 3600

    state["timerValue"] = inputValue
    timerElement.innerText = format_time(inputValue)  # Update the timer display with formatted time



# Function to handle the timer's start and stop functionality
def toggleTimer(event):
    if state["timerRunning"]:  # If timer is currently running
        timer.clear_interval(state["interval"])  # Stop the timer interval using the stored reference
        circleContainer.classList.remove('active')  # Remove the 'active' class which controls the animation
        contentDiv.classList.remove('active')
        document.select_one('.button').innerText = 'START'
        timerInputSection.style.display = "block"  # Display the timer input section when stopped
    else:  # If timer is not running
        # Function to decrement the timer value every second and update the display
        def decrement_timer():
            state["timerValue"] -= 1
            timerElement.innerText = format_time(state["timerValue"])  # Update the timer display
            # If timer reaches zero, stop it and reset the display
            if state["timerValue"] <= 0:
                timer.clear_interval(state["interval"])
                circleContainer.classList.remove('active')
                contentDiv.classList.remove('active')
                document.select_one('.button').innerText = 'START'

        # Start a timer interval that decrements the timer value every second
        state["interval"] = timer.set_interval(decrement_timer, 1000)
        document.select_one('.button').innerText = 'STOP'
        circleContainer.classList.add('active')  # Add 'active' class to initiate animations
        contentDiv.classList.add('active')
        timerInputSection.style.display = "none"  # Hide the timer input section when running

    # Toggle the timerRunning state
    state["timerRunning"] = not state["timerRunning"]


# Bind event listeners to HTML elements
# The 'bind' method attaches event handlers to HTML elements
document.select_one('.button').bind('click', toggleTimer)  # Attach the toggleTimer function to the START/STOP button
document.select_one('#setTimerValue').bind('click', setTimerValue)  # Attach setTimerValue function to the Set Timer button

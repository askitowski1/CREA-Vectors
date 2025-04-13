from psychopy import visual, event, core
import os 
import csv
import pandas as pd
import json
import random

w = 'word_list.csv'
c = 'ReformattedQuestions_copy.xlsx'

def load_word(file_name):
    df = pd.read_csv(file_name)
    word = df.iloc[10,0].capitalize()
    ex1 = df.iloc[10,1]
    ex2 = df.iloc[10,2]
    return word, ex1, ex2

def load_category(file_name):
    df = pd.read_excel(file_name)
    return df.iloc[:,0].tolist(), df.iloc[:,1].tolist(), df.iloc[:,2].tolist(), df.iloc[:,3].tolist()
    
cat_index = 0

word_text, ex1, ex2 = load_word(w)
category_list, cat_def_list, ex1_def_list, ex2_def_list = load_category(c)

#shuffle the categories but store the original order
original_category_list = category_list[:]
zipped_lists = list(zip(category_list, cat_def_list, ex1_def_list, ex2_def_list))
random.shuffle(zipped_lists)

category_list, cat_def_list, ex1_def_list, ex2_def_list = zip(*zipped_lists)
category_list = list(category_list)  
cat_def_list = list(cat_def_list)  
ex1_def_list = list(ex1_def_list)    
ex2_def_list = list(ex2_def_list)

stimuli = {} #make dictionary so object can keep its name

#make window and draw word
win = visual.Window(fullscr=True, color = "white")
mouse = event.Mouse(win=win)
instructions1 = visual.TextStim(win, text=f"""
Instructions

Thank you for participating in The Word Meaning Survey, an effort to discover how people think about and distinguish the meanings of words. Our goal is to collect judgments on many aspects of meaning for a large number of English words. Please do not complete this HIT unless you are a native English speaker.
This activity is a research study. Your participation is completely voluntary. To protect your privacy, we will not request from you or from Amazon Mechanical Turk any information that can be used to identify you, thus the responses you provide will be completely confidential.


In each session you will be assigned a word, for example, "shoe", and a sentence that illustrates how the word is used, such as "The boy put on his shoe." You will then be asked a series of questions about the meaning of the word. We estimate that it will take approximately 15 minutes to answer these questions for each word. PLEASE TAKE YOUR TIME. The information you provide will only be scientifically useful if you put some thought into it!


For example, you might be asked, "To what degree do you think of shoe as being heavy in weight?" For each such judgment, you will use a rating scale ranging from 0 to 6, with 0 meaning "not at all" and 6 meaning "very much". Because such scales are relative, you will also be given an example of a concept that would typically receive a high rating on the question, and an example that would typically receive a rating near the middle of the scale. For the question about heaviness, the high-rated example
is anvil and the medium example is bookcase. 

Given these definitions of heavy, you might rate shoe at about 1 on the scale.


Other judgments will be about more abstract aspects of meaning, such as, "To what degree do you think of shoe as someone or something that could help or benefit you or others?", with the example of a high-rated concept being cure, and the medium example being news. 

In this case you might give shoe a rating of 3 or 4, depending on how beneficial you think shoes are to people.


Other questions will be almost nonsensical, because they refer to aspects of word meaning that are not even applicable to your word. For example, you might be asked, "To what degree do you think of shoe as an event that has a predictable duration, whether short or long?",
with movie given as an example of a high-rated concept, and concert given as a medium-rated concept.

Since shoe refers to a static thing, not to an event of any kind, you should indicate either 0 or "Not Applicable" for this question.


Please give your best estimate for each rating. Ideally the collection of ratings you give for your word should allow another person to guess what the word is, something like the "20 questions" game.


Thanks again for participating in The Word Meaning Survey""", height = 0.03, wrapWidth = 1.3, color = 'black', pos = (0.0,0.0), alignText='left')
instructions1.draw()
win.flip()
core.wait(4)

# Allow user to advance after reading 
instructions1.text += "\n\n\nPress any key to begin."
instructions1.draw()
win.flip()
event.waitKeys()

instructions2 = visual.TextStim(win, text=f"""
Welcome to the experiment!





The word we would like you to rate is: "{word_text}"
As in "{ex1}"
As in "{ex2}"




For each of the following questions, you will use a rating scale ranging from 0 to 6, with 0 meaning "not at all" and 6 meaning "very much". Because such scales are relative, you will be given an example of a concept that would typically receive a rating at the high end of the scale, and an example that would typically receive a rating near the middle of the scale.




Please take your time and try to provide accurate ratings.




""",wrapWidth=1.5, height = .05, color = 'black', pos = (0.0,0.0))

# Draw and show the instructions
instructions2.draw()
win.flip()
core.wait(2)

# Allow participant to advance after reading 
instructions2.text += "\n\n\nPress any key to begin."
instructions2.draw()
win.flip()
event.waitKeys()



stimuli["word"] = visual.TextStim(win, text = word_text, pos = (0.0, 0.8), bold = True, height = .05, anchorHoriz = 'center', wrapWidth = 3, color='black', font="Helvetica")
stimuli["example1"] = visual.TextStim(win, text = "as in: " + ex1, pos = (0.0, 0.72), height = 0.05, anchorHoriz = 'center', wrapWidth = 3, color='black', font="Helvetica")
stimuli["example2"] = visual.TextStim(win, text = "as in: " + ex2, pos = (0.0, 0.68), height = 0.05, anchorHoriz = 'center', wrapWidth = 3, color='black', font="Helvetica")

#draw category info
stimuli['cat_def'] = visual.TextStim(win, text = "To what degree do you think of this as " + cat_def_list[cat_index], pos = (0.0, 0.2), bold = True, height = 0.05, wrapWidth = 1.5, color='black')
stimuli['ex1_cat'] = visual.TextStim(win, text = ex1_def_list[cat_index], pos = (0.0, 0), height = 0.05, wrapWidth = 1, anchorHoriz = 'center', color='black')
stimuli['ex2_cat'] = visual.TextStim(win, text = ex2_def_list[cat_index], pos = (0.0, -0.20), height = 0.05, wrapWidth = 1, anchorHoriz = 'center', color='black')

#can't concat a list so assigning it to a variable
inst_word = word_text
inst_cat = category_list[cat_index]

#instructions
stimuli['instructions'] = visual.TextStim(win, text = f"Your rating for {inst_word}", pos = (0.0, -.5), height = 0.05, wrapWidth = 3, anchorHoriz = 'center', color = 'black')

#make boxes
box_width = 0.1
box_height = 0.1
x_positions = [-0.625, -0.375, -0.125, 0.125, 0.375, 0.625, 0.875, -0.875]
buttons = []
y_position = -0.6
y_offset = -0.1
text_labels = ["Not at All", "", "", "Somewhat", "", "", "Very Much", "Not Applicable"]

#make button to advance
next_width = 0.2
next_height = 0.1
adv_btn = visual.ButtonStim(win, text="Advance", pos=(0.826, -0.88), size=(next_width, next_height), fillColor='white', color='white', autoLog=True)

for i, x_pos in enumerate(x_positions):
    if i == 7:
        button = visual.ButtonStim(win, text="N", pos=(x_pos, y_position), size=(box_width, box_height), borderColor = 'black', borderWidth = 5, fillColor='white', color='black', autoLog=True)
        label = visual.TextStim(win, text=text_labels[i], pos=(x_pos, y_position + y_offset), color='black', bold = False, height=0.05)
    elif i == 0:
        button = visual.ButtonStim(win, text="0", pos=(x_pos, y_position), size=(box_width, box_height), borderColor = 'black', borderWidth = 5, fillColor='white', color='black', autoLog=True)
        label = visual.TextStim(win, text=text_labels[i], pos=(x_pos, y_position + y_offset), color='black', bold = False, height=0.05)
    elif i == 3:
        button = visual.ButtonStim(win, text="3", pos=(x_pos, y_position), size=(box_width, box_height), borderColor = 'black', borderWidth = 5, fillColor='white', color='black', autoLog=True)
        label = visual.TextStim(win, text=text_labels[i], pos=(x_pos, y_position + y_offset), color='black', bold = False, height=0.05)
    elif i == 6:
        button = visual.ButtonStim(win, text="6", pos=(x_pos, y_position), size=(box_width, box_height), borderColor = 'black', borderWidth = 5, fillColor='white', color='black', autoLog=True)
        label = visual.TextStim(win, text=text_labels[i], pos=(x_pos, y_position + y_offset), color='black', bold = False, height=0.05)
    else:
        button = visual.ButtonStim(win, text=str(i), pos=(x_pos, y_position), size=(box_width, box_height), borderColor = 'black', borderWidth = 5, fillColor='white', color='black', autoLog=True)
        label_pos = (x_pos, y_position + y_offset)

    buttons.append((button, label))
def draw_buttons():
    for btn, label in buttons:
        btn.draw()
        label.draw()

current_btn = None
def track_buttons(selected_btn):
    global current_btn
    
    if current_btn is not None:
        buttons[current_btn][0].fillColor='white'
        
    buttons[selected_btn][0].fillColor='lightgrey'
    current_btn = selected_btn

def reset_buttons():
    global current_btn
    current_btn = None
    for btn, _ in buttons:
        btn.fillColor='white'
        
def adv_appear():
    adv_btn.draw()
adv_enabled = False
for stimuli_name, stimulus in stimuli.items():
    stimulus.draw()

valid_keys = ["n", "0", "1", "2", "3", "4", "5", "6"]
adv_key = "a"
quit_keys = ["q", " "]
response_map = {
    "n": 7,  
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6
}
# -----------------------------
# Button Practice Walkthrough
# -----------------------------
walkthrough_text = visual.TextStim(win, text="""
This is the rating scale you will use during the experiment.

You will rate each question using this scale from 0 ("Not at All") to 6 ("Very Much").

You can also select "N" for "Not Applicable".

Try clicking or pressing a number key now. Once you've selected, click 'Advance' or press the 'a' key to continue to the experiment .
""", wrapWidth=1.4, height=0.045, color='black', pos=(0, 0.75), alignText='left')

practice_adv_btn = visual.ButtonStim(win, text="Advance", pos=(0.826, -0.88), size=(0.2, 0.1), fillColor='white', color='white', autoLog=False)

def draw_walkthrough_interface():
    win.clearBuffer()
    walkthrough_text.draw()
    for btn, label in buttons:
        btn.draw()
        label.draw()
    if current_btn is not None:
        practice_adv_btn.fillColor = 'lightblue'
        practice_adv_btn.color = 'black'
    else:
        practice_adv_btn.fillColor = 'white'
        practice_adv_btn.color = 'white'
    practice_adv_btn.draw()
    win.flip()

# Reset buttons before walkthrough
reset_buttons()
current_btn = None
adv_enabled = False

# Walkthrough loop
while True:
    draw_walkthrough_interface()

    # Mouse press
    for i, (btn, label) in enumerate(buttons):
        if mouse.isPressedIn(btn):
            track_buttons(i)
            core.wait(0.2)

    # Key press
    keys = event.getKeys()
    for key in keys:
        if key in response_map:
            idx = response_map[key]
            track_buttons(idx)
            core.wait(0.2)

    # Advance logic (only works after they've selected)
    if current_btn is not None and (mouse.isPressedIn(practice_adv_btn) or 'a' in keys):
        reset_buttons()
        break
        
win.flip()
#draw everything
def update_display():
    win.clearBuffer()  # Clear previous screen
    stimuli["cat_def"].setText("To what degree do you think of this as " + cat_def_list[cat_index])
    stimuli["ex1_cat"].setText(ex1_def_list[cat_index])
    stimuli["ex2_cat"].setText(ex2_def_list[cat_index])
    
    inst_cat = category_list[cat_index]
    stimuli["instructions"].setText(f"Your rating for {inst_word}")
    
    for stim in stimuli.values():
        stim.draw()
    draw_buttons()
    adv_btn.draw()
    win.flip()


#make empty results list to record what happened
#this will be a list of dictionaries with the response to each category
results_list = {inst_word: {}}

# Inside the while loop
while cat_index < len(category_list):
    response = None
    while response is None:
        update_display()  # Ensure the screen is updated

        # Check for mouse clicks on response buttons
        for i, (btn, label) in enumerate(buttons):
            if mouse.isPressedIn(btn):
                track_buttons(i)
                adv_enabled = True
                adv_btn.fillColor = 'lightblue'
                adv_btn.color = 'black'
                response = str(i)
                original_index = original_category_list.index(category_list[cat_index])
                if word_text not in results_list:
                    results_list[word_text] = {}
                results_list[word_text][original_category_list[original_index]] = float(response_map.get(response, -1))
                core.wait(0.2)  

        # Check for key presses
        keys = event.getKeys()
        for key in keys:
            if key in valid_keys:
                current_btn_idx = response_map[key]
                track_buttons(current_btn_idx)
                # this feels very excessive. It works but surely theres a better way
                response = key
                print(response)
                print(type(response))
                adv_enabled = True
                adv_btn.fillColor = 'lightblue'
                adv_btn.color = 'black'
                original_index = original_category_list.index(category_list[cat_index])
                if word_text not in results_list:
                    results_list[word_text] = {}
                results_list[word_text][original_category_list[original_index]] = float(current_btn if key != "n" else -1)
            
        if adv_enabled and (adv_key in keys or mouse.isPressedIn(adv_btn)):
            cat_index += 1
            if cat_index >= len(category_list):
                print("You've completed all the ratings")
                break
            inst_cat = category_list[cat_index]
            reset_buttons()
            adv_btn.fillColor = 'white'  # Reset the color to white
            adv_btn.color = 'white'
            btn.fillColor = 'white'
#            core.wait(0.2)  # Wait a moment to show the reset color before continuing
            adv_enabled = False
            continue  # Continue to the next category

        # Check for quit keys
        if any(key in quit_keys for key in keys):
            print("Quitting and saving results...")
            break

    # Break the outer loop if the user quits or finishes
    if cat_index >= len(category_list) or any(key in quit_keys for key in keys):
        break

    #save dict as json
sorted_results = {}
for category in original_category_list:
    if category in results_list[word_text]:
        sorted_results[category] = results_list[word_text][category]
with open("results.json", "w") as outfile:
    json.dump(sorted_results, outfile)
print("results saved as json")
core.quit()

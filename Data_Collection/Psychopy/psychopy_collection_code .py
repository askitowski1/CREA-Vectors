from psychopy import visual, event, core
import os 
import csv
import pandas as pd
import json

w = 'word_list.csv'
c = 'category_define.csv'

def load_word(file_name):
    df = pd.read_csv(file_name)
    word = df.iloc[13,0]
    ex1 = df.iloc[13,1]
    ex2 = df.iloc[13,2]
    return word, ex1, ex2

def load_category(file_name):
    df = pd.read_csv(file_name)
    return df.iloc[:,0].tolist(), df.iloc[:,1].tolist(), df.iloc[:,2].tolist(), df.iloc[:,3].tolist(), df.iloc[:,4].tolist(), df.iloc[:,5].tolist()
    
cat_index = 0

word_text, ex1, ex2 = load_word(w)
category_list, cat_def_list, ex1_cat_list, ex1_def_list, ex2_cat_list, ex2_def_list = load_category(c)

stimuli = {} #make dictionary so object can keep its name

#make window and draw word
win = visual.Window(fullscr=True, color = "black")
mouse = event.Mouse(win=win)

stimuli["word"] = visual.TextStim(win, text = word_text + ": ", pos = (-0.15, 0.8), bold = True, height = .1)
stimuli["example1"] = visual.TextStim(win, text = ex1, pos = (0.15, 0.81), italic = True, height = -0.01)
stimuli["example2"] = visual.TextStim(win, text = ex2, pos = (0.15, 0.78), italic = True, height = -0.01)

#draw category info
stimuli['category'] = visual.TextStim(win, text = category_list[cat_index], pos = (0.0, 0.10), bold = True, height = .3, anchorHoriz = 'center')
stimuli['cat_def'] = visual.TextStim(win, text = cat_def_list[cat_index], pos = (0.0, -0.1), height = 0.07, wrapWidth = 3)
stimuli['ex1_cat'] = visual.TextStim(win, text = ex1_def_list[cat_index], pos = (0.0, -0.20), italic = True, height = -0.01, wrapWidth = 2, anchorHoriz = 'center')
stimuli['ex2_cat'] = visual.TextStim(win, text = ex2_def_list[cat_index], pos = (0.0, -0.25), italic = True, height = -0.01, wrapWidth = 2, anchorHoriz = 'center')

#can't concat a list so assigning it to a variable
inst_word = word_text
inst_cat = category_list[cat_index]

#instructions
stimuli['instructions'] = visual.TextStim(win, text = "Please click a button or press a key (1 = __ to 6 = __) as " + inst_word + " relates to " + inst_cat, pos = (0.0, -0.7), height = -0.01, wrapWidth = 3, anchorHoriz = 'center')

#make boxes
box_width = 0.1
box_height = 0.1
x_positions = [-0.7143, -0.4286, -0.1429, 0.1429, 0.4286, 0.7143]
buttons = []

for i, x_pos in enumerate(x_positions):
    button = visual.ButtonStim(win, text = str(i+1), pos = (x_pos, -0.8), size = (box_width, box_height), fillColor = 'grey', color = 'white', autoLog = True)
    buttons.append(button)
for btn in buttons:
    btn.draw()

for stimuli_name, stimulus in stimuli.items():
    stimulus.draw()
    
win.flip()
#draw everything
def update_display():
    win.clearBuffer()  # Clear previous screen
    stimuli["category"].setText(category_list[cat_index])
    stimuli["cat_def"].setText(cat_def_list[cat_index])
    stimuli["ex1_cat"].setText(ex1_def_list[cat_index])
    stimuli["ex2_cat"].setText(ex2_def_list[cat_index])
    
    inst_cat = category_list[cat_index]
    stimuli["instructions"].setText(f"Please click a button or press a key (1 = __ to 6 = __) as {inst_word} relates to {inst_cat}")
    
    for stim in stimuli.values():
        stim.draw()
    for btn in buttons:
        btn.draw()
    win.flip()

    
valid_keys = ["1", "2", "3", "4", "5", "6"]
quit_keys = ["q", " "]

#make empty results list to record what happened
#this will be a list of dictionaries with the response to each category
results_list = {inst_word: {}}

#letting the user click the button
#pressing the keys works as intended

while True:
    response = None
    while response is None:
        for i,btn in enumerate(buttons):
            if mouse.isPressedIn(btn):
                response = str(i+1)

                results_list[inst_word][inst_cat] = float(response)
                cat_index += 1
                if cat_index >= len(category_list):
                    print("You've completed all the ratings")
                    break
                inst_cat = category_list[cat_index]
                core.wait(.2) #this seems to help the clitchiness. Not sure if theres a better soln but it works with both clicks and presses 
                update_display()
                break
                
        keys = event.getKeys()
        if any(key in valid_keys for key in keys):
            response = keys[0]
            results_list[inst_word][inst_cat] = float(response)
            cat_index += 1
            if cat_index >= len(category_list):
                    print("You've completed all the ratings")
                    break
            inst_cat = category_list[cat_index]
            update_display()
        
        if any(key in quit_keys for key in keys):
            # Debug print before quitting
            print("Quitting and saving results...")
            break
            
    if cat_index >= len(category_list) or any(key in quit_keys for key in keys):  # auto stop if you reach the end 
        break #have to break out of the for loop and the while loop? 
        
    #save dict as json
with open("results.json", "w") as outfile:
    json.dump(results_list, outfile)
print("results saved as json")

core.quit()


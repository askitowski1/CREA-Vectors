// Begin Experiment
var word_text, ex1, ex2;
var category_list, cat_def_list, ex1_cat_list, ex1_def_list, ex2_cat_list, ex2_def_list;

function load_word(file_name) {
    let df = psychoJS.experiment.getData(file_name);
    word_text = df[2][0];
    ex1 = df[2][1];
    ex2 = df[2][2];
}

function load_category(file_name) {
    let df = psychoJS.experiment.getData(file_name);
    category_list = df[0];
    cat_def_list = df[1];
    ex1_cat_list = df[2];
    ex1_def_list = df[3];
    ex2_cat_list = df[4];
    ex2_def_list = df[5];
}

// Begin Routine
load_word('word_list.csv');
load_category('category_define.csv');

// Stimuli
var stimuli = {};
stimuli['word'] = new visual.TextStim({
    win: psychoJS.window,
    text: word_text + ": ",
    pos: [-0.15, 0.8],
    bold: true,
    height: 0.1
});
stimuli['example1'] = new visual.TextStim({
    win: psychoJS.window,
    text: ex1,
    pos: [0.15, 0.81],
    italic: true,
    height: -0.01
});
stimuli['example2'] = new visual.TextStim({
    win: psychoJS.window,
    text: ex2,
    pos: [0.15, 0.78],
    italic: true,
    height: -0.01
});

// Draw category info
stimuli['category'] = new visual.TextStim({
    win: psychoJS.window,
    text: category_list[0],
    pos: [0.0, 0.10],
    bold: true,
    height: 0.3,
    anchorHoriz: 'center'
});
stimuli['cat_def'] = new visual.TextStim({
    win: psychoJS.window,
    text: cat_def_list[0],
    pos: [0.0, -0.1],
    height: 0.07,
    wrapWidth: 3
});
stimuli['ex1_cat'] = new visual.TextStim({
    win: psychoJS.window,
    text: ex1_def_list[0],
    pos: [0.0, -0.20],
    italic: true,
    height: -0.01,
    wrapWidth: 2,
    anchorHoriz: 'center'
});
stimuli['ex2_cat'] = new visual.TextStim({
    win: psychoJS.window,
    text: ex2_def_list[0],
    pos: [0.0, -0.25],
    italic: true,
    height: -0.01,
    wrapWidth: 2,
    anchorHoriz: 'center'
});

// Instructions
stimuli['instructions'] = new visual.TextStim({
    win: psychoJS.window,
    text: "Please click a button or press a key (1 = __ to 6 = __) as " + word_text + " relates to " + category_list[0],
    pos: [0.0, -0.7],
    height: -0.01,
    wrapWidth: 3,
    anchorHoriz: 'center'
});

// Create buttons
var box_width = 0.1;
var box_height = 0.1;
var x_positions = [-0.7143, -0.4286, -0.1429, 0.1429, 0.4286, 0.7143];
var buttons = [];
for (var i = 0; i < x_positions.length; i++) {
    var button = new visual.ButtonStim({
        win: psychoJS.window,
        text: (i + 1).toString(),
        pos: [x_positions[i], -0.8],
        size: [box_width, box_height],
        fillColor: 'grey',
        color: 'white'
    });
    buttons.push(button);
}

// Initialize mouse and keyboard response
var mouse = new core.Mouse();
var valid_keys = ["1", "2", "3", "4", "5", "6"];
var quit_keys = ["q", " "];
var results_list = [{'word': word_text}];
var cat_index = 0;

function update_display() {
    stimuli['category'].setText(category_list[cat_index]);
    stimuli['cat_def'].setText(cat_def_list[cat_index]);
    stimuli['ex1_cat'].setText(ex1_def_list[cat_index]);
    stimuli['ex2_cat'].setText(ex2_def_list[cat_index]);

    stimuli['instructions'].setText("Please click a button or press a key (1 = __ to 6 = __) as " + word_text + " relates to " + category_list[cat_index]);

    for (var stim in stimuli) {
        stimuli[stim].draw();
    }
    for (var btn of buttons) {
        btn.draw();
    }
    psychoJS.window.flip();
}

// Update the display
update_display();

// Main loop for capturing response
while (true) {
    var response = null;

    // Check for button clicks
    for (var i = 0; i < buttons.length; i++) {
        if (mouse.isPressedIn(buttons[i])) {
            response = (i + 1).toString();
            results_list[0][category_list[cat_index]] = response;
            cat_index += 1;
            if (cat_index >= category_list.length) {
                break;
            }
            update_display();
            core.wait(0.2); // Delay to prevent glitches
            break;
        }
    }

    // Check for key presses
    var keys = event.getKeys();
    if (keys.length > 0) {
        if (valid_keys.includes(keys[0])) {
            response = keys[0];
            results_list[0][category_list[cat_index]] = response;
            cat_index += 1;
            if (cat_index >= category_list.length) {
                break;
            }
            update_display();
        }
    }

    // Check for quitting
    if (keys.includes(quit_keys[0]) || keys.includes(quit_keys[1])) {
        console.log("Quitting and saving results...");
        break;
    }
}

// Save results as JSON
var json_result = JSON.stringify(results_list);
fs.writeFileSync('results.json', json_result);
console.log("Results saved as JSON");

core.quit();

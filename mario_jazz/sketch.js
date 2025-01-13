let markov; // Markov chain instance
let midiTokens1 = [];
let midiTokens2 = [];
let midiLoaded = 0; // Counter to track the loading of MIDI files

function preload() {
  // Load MIDI files and parse them into tokens
  loadBytes('./midi/Only-The-Lonely-2.mid', data => {
    midiTokens1 = parseMidi(data.bytes);
    console.log("MIDI 1 Tokens:", midiTokens1);
    midiLoaded++;
  });

  loadBytes('./midi/Never-Gonna-Give-You-Up-1.mid', data => {
    midiTokens2 = parseMidi(data.bytes);
    console.log("MIDI 2 Tokens:", midiTokens2);
    midiLoaded++;
  });
}

function setup() {
  createCanvas(800, 200);
  noLoop(); // Ensure the draw loop doesn't run continuously
}

function draw() {
  background(220);

  // Check if both MIDI files are loaded
  if (midiLoaded < 2) {
    textSize(16);
    fill(0);
    text("Loading MIDI files...", width / 2 - 80, height / 2);
    return;
  }

  // Initialize Markov chain
  markov = new RiMarkov(2, false, true);
  markov.loadTokens(midiTokens1);

  // Generate and visualize the continuation
  let continuation = markov.generateTokens(50);
  visualizeSequence(continuation, 50, "Generated Continuation");

  // Create a mash-up sequence
  let mashupTokens = createMashup(midiTokens1, midiTokens2);
  visualizeSequence(mashupTokens, 150, "Mash-Up Sequence");
}

// Function to parse MIDI files into note tokens
function parseMidi(bytes) {
  try {
    let midi = new Midi(bytes);
    let notes = [];
    midi.tracks.forEach(track => {
      track.notes.forEach(note => notes.push(note.name)); // Extract note names
    });
    return notes;
  } catch (error) {
    console.error("Error parsing MIDI:", error);
    return [];
  }
}

// Function to create a mash-up sequence using two token sets
function createMashup(tokens1, tokens2) {
  let combinedTokens = [...tokens1, ...tokens2];
  let mashupMarkov = new RiMarkov(2, false, true);
  mashupMarkov.loadTokens(combinedTokens);
  return mashupMarkov.generateTokens(50);
}

// Function to visualize a sequence
function visualizeSequence(sequence, yOffset = 50, title = "Generated Sequence") {
  let x = 10;
  textSize(12);
  fill(0);
  text(title, 10, yOffset - 20);

  sequence.forEach(token => {
    text(token, x, yOffset);
    x += 30; // Space between tokens
  });
}

// Function to save a generated sequence as a MIDI file
function saveSequenceAsMidi(sequence, fileName) {
  let midi = new Midi();
  let track = midi.addTrack();
  sequence.forEach((note, index) => {
    track.addNote({
      name: note,
      time: index * 0.5,
      duration: 0.5,
    });
  });
  saveBytes(midi.toArray(), fileName);
}

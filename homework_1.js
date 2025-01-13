let json, animals;

function preload() {
  json = loadJSON('data/common.json');
}

function setup() {
  createCanvas(320, 80);
  animals = json.animals;
  // Sanity check: Print syllable count for all animals names loaded
  // for (let animal of animals) {
  //   print(animal + ": " + countSyllables(animal));
  // }
  textAlign(CENTER, CENTER);
}

function draw() {
  background(220);
  let lines = stanza();
  text(lines, width/2, height/2);
  frameRate(0.2);
}

function stanza() {
  let house = random(['Gryffindor', 'Ravenclaw', 'Hufflepuff', 'Slytherin']);
  
  // TODO:
  // update the following to choose animals with syllable counts
  // 1. use countSyllables() function (below) to choose animal1 with 3 syllables
  // 2. use countSyllables() function (below) to choose animal2 with 1 syllable
  
  let animal1 = random(animals);
  let animal2 = random(animals);
  
  let adj = '¯\\_(ツ)_/¯';
  
  // TODO:
  // replace adj with adjective with 1 syllable rhyming with animal2
  // 1. check out the RiTa.rhymes() function to get rhyming words
  // 2. use the isAdjective() function (below) to filter rhyming words
  // 3. choose a random rhyming adjective and/or check one exists
  // 4. if no rhyming adjective found, try choosing a different animals2
  
  return "The body of " + a(animal1) +
    ", the wisdom of " + a(animal2) + "\n" +
    "I'm putting you in " + house +
    " for you are really " + adj;
}

// !!! Warning: Ugly hack for RiTa bug for some words. !!!
// List of words that RiTa gets the syllables wrong,
// where each entry is {"word": count}
const badcounts = [
  {"cougar": 2},
  {"orangutan": 4},
  {"reindeer": 2}
];

function countSyllables(word) {
  // !!! Warning: Ugly hack for RiTa bug for some words. !!!
  if (badcounts.some(obj => obj[word])) {
    return badcounts.find(obj => obj[word])[word];
  }
  // Replace hyphens with spaces
  const noHyphens = word.replaceAll("-", " "); 
  // Get syllables string
  const syllables = RiTa.getSyllables(noHyphens);
  // Split syllables on "/" (syllables) and " " (words)
  return syllables.split(/[\/ ]/).length;
}

function a(word) {
  let result = 'a';
  const noHyphens = word.replaceAll("-", " "); // Replace hyphens with spaces
  const firstPhoneme = RiTa.getPhonemes(noHyphens)[0];
  if (['a','e','i','o','u'].includes(firstPhoneme)) {
    result = 'an';
  }
  return result + ' ' + word;
}

function isAdjective(word) {
  // return true if word is tagged 'jj' (adjective)
  return RiTa.getPosTags(word)[0] === 'jj';
}
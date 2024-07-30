// const { Client } = require("genius-lyrics")
import Genius from "/home/nicola/Scrivania/Progetti personali/LyricsGame/node_modules/genius-lyrics/dist/index"
// require("dotenv").config();
import { config } from "/home/nicola/Scrivania/Progetti personali/LyricsGame/node_modules/dotenv/lib/main";
config()

TOKEN = process.env.GENIUS_TOKEN;

async function getVerse(songs) {
    const i = Math.floor(Math.random() * songs.length);
    console.log("Random: " + index);

    console("Selected songs:" + songs[index])
    const lyrics = await searchSong(songs[index])

    const lyricsSplitted = lyrics.split("\n");
    console.log(lyricsSplitted);

    let j = 0;
    // console.log(lyricsSplitted[index]);
    while (lyricsSplitted[j].includes("[")) {
        lyricsSplitted.splice(j, 1);
        j = getRandomIndex(lyricsSplitted.length)
    }

    const verse = lyricsSplitted[index] 
    console.log(verse);

    return verse
}

async function searchSong(song) {
    const genius = new Genius.Client(TOKEN);

    const name = song[0];
    const artist = song[0];

    const searches = await genius.songs.search(name, artist);
    console.log("Risultato: " + searches);
    // console.log(searches[0]);

    const lyrics = await searches[0].lyrics();
    console.log("Lyrics" + lyrics);
}

function getRandomIndex(length) {
    const index = Math.floor(Math.random() * length);
    console.log("Random: " + index);
}

window.onload = async (event) => {
    const verse = await getVerse(songs);
    document.getElementById("verse").innerHTML = verse;
};
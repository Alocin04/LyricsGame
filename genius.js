const { Client } = require("genius-lyrics")

require("dotenv").config();

async function searchSong() {
    const genius = new Client(process.env.GENIUS_TOKEN);

    const searches = await genius.songs.search("Sono Salvato");
    // console.log(searches);
    // console.log(searches[0]);

    const lyrics = await searches[0].lyrics();
    // console.log(lyrics);

    const lyricsSplitted = lyrics.split("\n");
    // console.log(lyricsSplitted);

    let index = 0;
    // console.log(lyricsSplitted[index]);
    while (lyricsSplitted[index].includes("[")) {
        lyricsSplitted.splice(index, 1);
        index = Math.floor(Math.random() * lyricsSplitted.length);
        console.log("Random: " + index);
    }
    console.log(lyricsSplitted[index]);
}

searchSong()
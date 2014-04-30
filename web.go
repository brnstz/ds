package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io/ioutil"
	"net/http"
	"net/url"
	"path/filepath"
)

var rootDir = "/home/bseitz/proj/music"
var jsonCt = "application/json; charset=utf-8"
var htmlCt = "text/html; charset=utf-8"
var spotifyUrl = "https://ws.spotify.com/search/1/track.json"

type clusters []cluster

type spotifyResp struct {
	Tracks []struct {
		Href string
	}
}

type cluster struct {
	Label          int     `json:"label"`
	MedianDistance float32 `json:"median_distance"`
	MedianTempo    float32 `json:"median_tempo"`
	ModeScores     struct {
		Major int `json:"major"`
		Minor int `json:"minor"`
	} `json:"mode_scores"`
	NumTracks int             `json:"num_tracks"`
	TopTerms  [][]interface{} `json:"top_terms"`
	TopWords  [][]interface{} `json:"top_words"`
	Tracks    []struct {
		AlbumName  string  `json:"album_name"`
		ArtistName string  `json:"artist_name"`
		Distance   float32 `json:"distance"`
		SongName   string  `json:"song_name"`
		TrackId    string  `json:"track_id"`
	}
}

var clusterHtml = template.Must(template.New("clusterHtml").Parse(`<html>
    <head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>

        <script>
            function listenTo(artist, song, track) {
                /*
                console.log(artist);
                console.log(song);
                console.log(track);
                */
                var req = {
                    "artist": artist,
                    "song": song
                };

                $.get("/listen?" + $.param(req), null, function(data) {
                    $("div#musicbox" + track).html(data);
                }, "html");

                return false;
            }
        </script>
    </head>

    <style>
        html, body, form, fieldset, table, tr, td, img {
            font: 100%/150% calibri,helvetica,sans-serif;
        }

        input, button, select, textarea, optgroup, option {
            font-family: inherit;
            font-size: inherit;
            font-style: inherit;
            font-weight: inherit;
        }
    </style>
    <body>

	<ul>
	{{ range $ }}
		<li>Cluster {{ .Label }}</li>
			<ul>
				<li>Median Distance from Center: {{ .MedianDistance }}</li>
				<li>Median Tempo: {{ .MedianTempo }}</li>
                <li>Major Key: {{ .ModeScores.Major }}</li>
                <li>Minor Key: {{ .ModeScores.Minor }}</li>
                <li>Track Count: {{ .NumTracks }}</li>
                <li>Terms: {{ .TopTerms }}</li>
                <li>Words: {{ .TopWords }}</li>
                <li>Closest 50 Tracks to Center:</li>
                <ul>
                    {{ range .Tracks }}
                    <li>{{ .ArtistName }}: {{ .SongName}} ( {{.Distance}} )
                        <a href="javascript:listenTo('{{ .ArtistName }}', '{{ .SongName }}', '{{ .TrackId}}');>Listen!</a> <div id="musicbox{{ .TrackId}}"></div>
                    </li>
                    {{ end }}
                </ul>
			</ul>
	{{ end }}
	</ul>

	</body>
</html>`))

/*
Maybe try this later:
                    <li>{{ .ArtistName }}: {{ .SongName}} <a href="javascript:listenTo("{{ .ArtistName }}", "{{ .SongName }}", "{{ .TrackId}}"); return false;">Listen!</a></li>

    <script type="javascript">
        var svg = d3.select("terms{{ .Label}}").append("svg")
            .attr("width", 500)
            .attr("width", 500)
            .attr("class", "bubble");
        {{ range .TopTerms }}
            svg.append("title").text("{{ .0 }} {{ .1}}");
        {{ end }}
    </script>
*/

func main() {

	http.HandleFunc("/cluster", func(w http.ResponseWriter, r *http.Request) {
		//"100ktracks.csv_500"

		f := filepath.Join(rootDir, fmt.Sprintf("clusters_by_distance_%v.json", r.FormValue("file")))
		b, err := ioutil.ReadFile(f)

		if err != nil {
			fmt.Fprint(w, err)
			return
		}

		var c clusters
		err = json.Unmarshal(b, &c)

		if err != nil {
			fmt.Fprint(w, err)
			return
		}

		for i, _ := range c {
			if len(c[i].Tracks) > 50 {
				c[i].Tracks = c[i].Tracks[0:50]
			}
		}

		w.Header().Add("Content-Type", htmlCt)

		clusterHtml.Execute(w, c)
	})

	http.HandleFunc("/listen", func(w http.ResponseWriter, r *http.Request) {
		// Get artist and song from our page
		artist := r.FormValue("artist")
		song := r.FormValue("song")

		// Create spotify url
		u, _ := url.Parse(spotifyUrl)
		q := u.Query()
		q.Set("q", fmt.Sprintf("%v %v", artist, song))
		u.RawQuery = q.Encode()

		resp, err := http.Get(u.String())

		// Can't run http get
		if err != nil {
			fmt.Fprint(w, err)
			return
		}
		defer resp.Body.Close()

		b, err := ioutil.ReadAll(resp.Body)

		// Can't read response
		if err != nil {
			fmt.Fprint(w, err)
			return
		}

		var sr spotifyResp
		err = json.Unmarshal(b, &sr)

		// Can't decode json
		if err != nil {
			fmt.Fprint(w, err)
			return
		}

		// No tracks
		if len(sr.Tracks) < 1 {
			return
		}

		fmt.Fprintf(w, `<iframe src="https://embed.spotify.com/?uri=%v" frameborder="0" allowtransparency="true"></iframe>`, sr.Tracks[0].Href)

	})

	http.ListenAndServe(":53172", nil)
}

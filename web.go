package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io/ioutil"
	"net/http"
	"path/filepath"
)

var rootDir = "/home/bseitz/proj/music"
var jsonCt = "application/json; charset=utf-8"
var htmlCt = "text/html; charset=utf-8"

type clusters []cluster

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
		<li>
			<ul>
				<li>Median Distance: {{ .MedianDistance }}</li>
				<li>Median Tempo: {{ .MedianTempo }}</li>
                <li>Major Key: {{ .ModeScores.Major }}</li>
                <li>Minor Key: {{ .ModeScores.Minor }}</li>
                <li>Tracks: {{ .NumTracks }}</li>
                <li>Terms: {{ .TopTerms }}</li>
                <li>Words: {{ .TopWords }}</li>
			</ul>
		</li>
	{{ end }}
	</ul>

	</body>
</html>`))

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

		w.Header().Add("Content-Type", htmlCt)

		clusterHtml.Execute(w, c)

	})

	http.ListenAndServe(":53172", nil)
}
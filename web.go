package main

import (
	//"encoding/json"
	"fmt"
	"net/http"
)

var ROOT = "/home/bseitz/proj/music"

func main() {

	http.HandleFunc("/cluster", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "hello")
	})
	http.ListenAndServe(":53172", nil)
}

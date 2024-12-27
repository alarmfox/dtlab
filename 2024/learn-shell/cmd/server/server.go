package main

import (
	"encoding/base64"
	"fmt"
	"net/http"
	"time"
)

func main() {

	http.HandleFunc("GET /shell", func(w http.ResponseWriter, r *http.Request) {
		p := r.URL.Query()
		token := p.Get("code")
		str, err := base64.StdEncoding.DecodeString(token)
		if err != nil {
			http.Error(w, fmt.Sprintf("%v", err), 500)
		}
		
		dur, err := time.ParseDuration(string(str))
		if err != nil {
			http.Error(w, fmt.Sprintf("%v", err), 500)
		}
    w.Write([]byte(fmt.Sprintf("Not bad! Your score is: %d\n", dur)))
	})

	if err := http.ListenAndServe("0.0.0.0:3000", nil); err != nil {
		fmt.Print(err)
	}
}

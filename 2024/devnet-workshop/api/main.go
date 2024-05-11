package main

import (
	"context"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	key          = "0InfNl5WZuR++sOUD4otAw=="
	session      = "sessionid"
	cookieLength = 20
)

type ctxKeyType int
type ctxValueType string

type Interface struct {
	Name        string `json:"name"`
	Address     string `json:"address"`
	Netmask     string `json:"netmask"`
	Description string `json:"description"`
	Status      string `json:"status"`
}

type Device struct {
	ID         int         `json:"id"`
	Serial     string      `json:"serial"`
	Model      string      `json:"model"`
	Type       string      `json:"type"`
	Interfaces []Interface `json:"interfaces"`
}

type Database struct {
	devices    map[int]Device
	mu         sync.RWMutex
	nextInt    int
	lastAccess time.Time
}

var (
	sessions      map[string]*Database
	listenAddress = flag.String("listen-addr", "0.0.0.0:3000", "Listen address for the server")
)

func initDatabase() *Database {
	db := make(map[int]Device)
	db[1] = Device{
		ID:     1,
		Serial: "CAT-2960-5483221",
		Model:  "Catalyst-2960x-48p",
		Type:   "SWL2",
		Interfaces: []Interface{
			{
				Name:        "VLAN1",
				Address:     "192.168.1.100",
				Netmask:     "255.255.255.0",
				Description: "A VLAN",
				Status:      "Administrative down",
			},
		},
	}
	db[2] = Device{
		ID:     2,
		Serial: "CAT-2960-5483221",
		Model:  "Catalyst-2960x-48p",
		Type:   "SWL2",
		Interfaces: []Interface{
			{
				Name:        "VLAN1",
				Address:     "192.168.1.100",
				Netmask:     "255.255.255.0",
				Description: "A VLAN",
				Status:      "Administrative down",
			},
		},
	}

	return &Database{
		devices: db,
		mu:      sync.RWMutex{},
		nextInt: 3,
	}
}

func main() {

	flag.Parse()

	var (
		logger = slog.New(slog.NewJSONHandler(os.Stdout, nil))
		ctx    = context.Background()
	)

	sessions = make(map[string]*Database)

	server := makeHttpServer(ctx, *listenAddress)
	logger.Info("listening on", "address", *listenAddress)

	if err := server.ListenAndServe(); err != nil {
		logger.Error("listen error", "error", err)
		os.Exit(2)
	}

}

func makeHttpServer(ctx context.Context, httpServer string) *http.Server {

	mux := http.NewServeMux()

	var (
		getAllHandler = http.HandlerFunc(getAll)
		deleteHandler = http.HandlerFunc(deleteDevice)
	)
	mux.Handle("GET /", setSession(getAllHandler))

	mux.Handle("DELETE /{id}", setSession(auth(deleteHandler)))

	server := http.Server{
		Addr:              httpServer,
		ReadHeaderTimeout: 10 * time.Second,
		IdleTimeout:       60 * time.Second,
		WriteTimeout:      5 * time.Second,
		Handler:           mux,
	}

	return &server
}

func getAll(w http.ResponseWriter, r *http.Request) {

  database, err := getDatabase(r.Context())
  if err != nil {
    http.Error(w, "internal error", http.StatusInternalServerError)
    return
  }
	database.mu.RLock()
	defer database.mu.RUnlock()
	results := make([]Device, len(database.devices))
	i := 0
	for _, v := range database.devices {
		results[i] = v
		i += 1
	}
	if err := writeJson(w, results); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func deleteDevice(w http.ResponseWriter, r *http.Request) {

  database, err := getDatabase(r.Context())
  if err != nil {
    http.Error(w, "internal error", http.StatusInternalServerError)
    return
  }
	database.mu.Lock()
	defer database.mu.Unlock()
	id := r.PathValue("id")
	idInt, err := strconv.Atoi(id)
	if err != nil {
		http.Error(w, "Invalid id", http.StatusBadRequest)
		return
	}
	_, exists := database.devices[idInt]

	if !exists {
		http.Error(w, "Device not found", http.StatusNotFound)
		return
	}

	delete(database.devices, idInt)
	w.WriteHeader(http.StatusNoContent)
}

func auth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token := r.Header.Get("Authorization")
		parts := strings.Split(token, " ")
		if len(parts) != 2 {
			http.Error(w, "Bad authorization", http.StatusUnauthorized)
			return
		}

		if parts[0] != "Bearer" {
			http.Error(w, "Bad authorization", http.StatusUnauthorized)
			return
		}

		if parts[1] != key {
			http.Error(w, "Bad authorization", http.StatusUnauthorized)
			return
		}

		next.ServeHTTP(w, r)
	})
}

func writeJson(w http.ResponseWriter, data any) error {
	w.Header().Add("Content-Type", "application/json")

	return json.NewEncoder(w).Encode(data)
}

func setSession(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie(session)
		if errors.Is(err, http.ErrNoCookie) {
			token := getToken(cookieLength)
			sessions[token] = initDatabase()
			cookie = &http.Cookie{
				Name:     session,
				Value:    token,
				HttpOnly: true,
			}
		} else if err != nil{
			slog.Error("error", "cookie error", err)
			return
		}

		ctx := context.WithValue(r.Context(), ctxKeyType(1), cookie.Value)
		r = r.WithContext(ctx)
		http.SetCookie(w, cookie)
		next.ServeHTTP(w, r)

	})

}

func getToken(length int) string {
	randomBytes := make([]byte, 32)
	_, err := rand.Read(randomBytes)
	if err != nil {
		panic(err)
	}
	return base64.StdEncoding.EncodeToString(randomBytes)[:length]
}

func getDatabase(ctx context.Context) (*Database, error){
	token := ctx.Value(ctxKeyType(1))
	if token == nil {
		return nil, fmt.Errorf("error db not present") 
	}

	database := sessions[token.(string)]
  if database == nil {
    database = initDatabase()
    sessions[token.(string)] = database
  }
  return database, nil

}

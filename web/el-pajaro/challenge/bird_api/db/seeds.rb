
birds = Bird.create([
    {name: "Peregrine Falcon", classification: "Falconidae", description: "The Peregrine Falcon is a small bird of prey native to many places around the world.", image_url: "https://images.unsplash.com/photo-1615574389508-3cfffaf11b9c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1471&q=80"},
    {name: "Domestic Grey Goose", classification: "Anatidae", description: "Honk", image_url:"https://images.unsplash.com/photo-1603985467507-597133f237df?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1469&q=80"},
    {name: "Resplendant Quetzal", classification: "Trogonidae", description: "The Resplendant Quetzal are small birds native to Mexico, well known for their beautiful and colorful plumage.", image_url: "https://images.unsplash.com/photo-1551647318-f0b1dfea688a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=897&q=80"},
    {name: "Rainbow Lorikeet", classification: "Psittaculidae", description: "Rainbow Lorikeets are small, colorful parrots native to Australia. They chirp upside down.", image_url: "https://images.unsplash.com/photo-1538440367084-0a21cb983cee?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1405&q=80"}
])  

admin = User.create(username: "admin", password: "", email: "maple{Birds_of_a_f3ath3r_fl0ck_together}@notreal.ca", favbird_id: 1)
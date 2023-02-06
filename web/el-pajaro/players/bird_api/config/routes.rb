
Rails.application.routes.draw do
  root "birds#index"
  get "/bird/get", to: "birds#readOneBird"
  post "/user/create", to: "users#createUser"
  get "/user/find", to: "users#readUser"
  post "/user/edit", to: "users#updateUser"
  post "/user/delete", to: "users#deleteUser"
end
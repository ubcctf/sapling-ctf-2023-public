class BirdsController < ApplicationController

    def index
        birds = Bird.all
        render json: birds
      end

    def readOneBird
        bird_req = params[:name]
        bird = Bird.lock.find_by(name: bird_req)
        render json: bird
    end
end

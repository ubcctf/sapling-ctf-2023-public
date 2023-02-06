class UsersController < ApplicationController
    def createUser
        req_body = JSON.parse(request.body.read)
        if User.exists?(username: req_body["username"])
            render json: '{"success":0, "message": "User already exists."}', :status => 400
            return
        end
        user = User.create(username: req_body["username"], password: req_body["password"], email: req_body["email"], favbird_id: ["favbird"])
        jwt = JsonWebToken.encode(user_id: user.id)
        render json: jwt, :status => 200 
    end

    def readUser
        if request.headers['Authorization'].present?
            auth = JsonWebToken.decode(request.headers['Authorization'].split(' ').last)
            if User.exists?(auth[:user_id])
                puts "ok?"
                if User.exists?(id: params[:id])
                    user = User.lock.where(id: params[:id]).first
                    render json: user, :status => 200
                    return
                end
            else
                puts "where am i "
                render json: '{"success":0, "message": "user not found"}', :status => 400
                return
            end
        else
            puts "bad"
            render json: '{"success":0, "message": "not logged in"}', :status => 403
            return
        end

    end

    def updateUser
        if request.headers['Authorization'].present?
            auth = JsonWebToken.decode(request.headers['Authorization'].split(' ').last)
            if User.exists?(auth[:user_id])
                if User.exists?(id: params[:id])
                    user = User.lock.where(id: params[:id]).first
                    req_body = JSON.parse(request.body.read)
                    if req_body["id"]
                        render json: '{"success":0, "message":"cannot edit ID"}', :status => 400
                        return
                    end
                    req_body.each { |k, v| user[k] = req_body[k] }
                    user.save
                    render json: user, :status => 200
                    return
                end
            else
                render json: '{"success":0, "message": "user not found"}', :status => 400
                return
            end
        else
            render json: '{"success":0, "message": "not logged in"}', :status => 403
            return
        end

    end
end

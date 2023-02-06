FROM ruby:3.2.0
WORKDIR /app/pajaro
RUN gem install rails bundler
COPY bird_api/Gemfile /Gemfile
COPY bird_api .
RUN chmod -R 777 /app/pajaro && bundle install && rake db:setup


EXPOSE 3000
CMD ["rails", "server", "-b", "0.0.0.0"]
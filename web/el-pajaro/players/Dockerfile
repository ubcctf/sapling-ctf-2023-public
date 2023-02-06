FROM ruby:3.2.0
WORKDIR /app/pajaro
RUN gem install rails bundler
COPY bird_api/Gemfile /Gemfile
COPY bird_api/Gemfile.lock /Gemfile.lock
COPY bird_api .
RUN bundle install
RUN rake db:setup

EXPOSE 3000
CMD ["rails", "server", "-b", "0.0.0.0"]
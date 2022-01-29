docker build -t img_bot .
docker run -d --rm -e "TOKEN=$TOKEN" --name img_bot_cont img_bot
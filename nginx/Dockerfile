# Fetching the latest nginx image
FROM nginx:1.23-alpine

# Removing default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copying our nginx.conf
COPY nginx.conf /etc/nginx/conf.d

# Expose port 80 (or any other port as needed)
EXPOSE 80
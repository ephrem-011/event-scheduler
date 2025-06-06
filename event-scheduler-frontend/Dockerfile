# frontend/Dockerfile
FROM nginx:alpine

# Remove default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the production build into Nginx's default HTML directory
COPY dist/ /usr/share/nginx/html/

# Expose port 80 to the host
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]




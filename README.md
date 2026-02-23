# Google OAuth Implementation

This document outlines the authentication flow, data model, and security requirements for the Google OAuth integration.

## 1. Authentication Sequence

The following diagram illustrates the interaction between the User, our API, and the Google Provider.

**Note:** The highlighted section indicates steps implicitly handled by the browser/redirects.

```mermaid
sequenceDiagram
    actor User as User | Browser
    participant API
    participant Google as Provider (Google)

    User->>API: /auth/login/google
    API->>User: redirect to google (code 302)
    User->>Google: login to google account
    
    %% Implicitly implemented steps (highlighted in light red)
    rect rgb(255, 245, 245)
    Note right of User: Implicitly Implemented (Redirects)
    Google->>User: 302 Redirect /auth/callback/google?code=..
    User->>API: GET /auth/callback/google?code=...
    end
    
    API->>Google: POST: https://oauth2.googleapis.com/token
    
    Note right of API: Payload:<br/>{ "code": "AuthCode_987...",<br/>"client_id": "id",<br/>"client_secret": "sec",<br/>"redirect_uri": "auth/callback/google",<br/>"grant_type": "authorization_code" }
    
    Google-->>API: return id token
    
    API->>API: validate + check login / sign up
    API->>User: redirect to dashboard
```

## 2. Data Model

The schema separates the core `User` identity from the `Federated` identity provider details.

```mermaid
classDiagram
    class User {
        +String Id
        +String Email
        +String Password
    }

    class Federated {
        +String Id
        +String UserId (FK)
        +String Provider
        +String SubjectId
    }

    %% Relationship
    User "1" -- "0..*" Federated : has
```

## 3. Security Configuration

### RSA Key Generation
Use the following OpenSSL commands to generate the key pair required for signing and validating JWTs.

```bash
# 1. Generate the private key (2048 bits)
openssl genrsa -out private.pem 2048

# 2. Extract the public key from the private key
openssl rsa -in private.pem -pubout -out public.pem
```

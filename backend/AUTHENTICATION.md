# Supabase Authentication Integration Guide

## Overview

The ReadWise backend now uses **Supabase JWT token authentication** to identify and authorize users. All protected endpoints require a valid JWT token from Supabase.

## Setup

### 1. Get Your Supabase JWT Secret

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **API**
3. Copy the **JWT Secret** (this is used to verify tokens)
4. Add it to your `.env` file:

```env
SUPABASE_JWT_SECRET=your-jwt-secret-here
```

### 2. Install Dependencies

The required package `PyJWT` has been added to `requirements.txt`. Install it with:

```bash
pip install PyJWT
```

## How It Works

### Authentication Flow

1. **User logs in** via Supabase Auth (handled by frontend)
2. **Supabase returns a JWT token** containing the user's ID in the `sub` claim
3. **Frontend sends the token** in the `Authorization` header with each request:
   ```
   Authorization: Bearer <jwt-token>
   ```
4. **Backend verifies the token** using the JWT secret and extracts the user ID
5. **User ID is used** to set `owner_id` when creating books/chapters

### Protected Endpoints

The following endpoints now require authentication:

- `POST /books` - Upload a book (requires valid JWT)

All other endpoints currently don't require authentication, but you can easily add it by adding the `current_user_id: str = Depends(get_current_user_id)` parameter.

## Frontend Integration

Your frontend should:

1. **Obtain the JWT token** after user login using Supabase client:
   ```javascript
   const { data: { session } } = await supabase.auth.getSession()
   const token = session?.access_token
   ```

2. **Include the token in API requests**:
   ```javascript
   const response = await fetch('http://localhost:8000/books', {
     method: 'POST',
     headers: {
       'Authorization': `Bearer ${token}`,
     },
     body: formData
   })
   ```

## Testing

### Using curl

```bash
# First, get a token from Supabase (via your frontend or Supabase client)
TOKEN="your-supabase-jwt-token"

# Upload a book
curl -X POST http://localhost:8000/books \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf"
```

### Using the verification script

Update `verify_rls.py` to use a real JWT token:

```python
# Get a real token from Supabase
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

headers = {'Authorization': f'Bearer {TOKEN}'}
response = requests.post(f"{BASE_URL}/books", files=files, headers=headers)
```

## Error Responses

### 401 Unauthorized - Missing Token
```json
{
  "detail": "Not authenticated"
}
```

### 401 Unauthorized - Invalid Token
```json
{
  "detail": "Invalid token: Signature verification failed"
}
```

### 401 Unauthorized - Expired Token
```json
{
  "detail": "Token has expired"
}
```

## Row Level Security (RLS)

With this authentication in place, you can now:

1. **Enable RLS on Supabase** tables (`books` and `chapters`)
2. **Create policies** that check `owner_id = auth.uid()`
3. **Ensure data privacy** - users can only access their own books

### Example RLS Policies

```sql
-- Books: owner can read
CREATE POLICY "Books: owner can read"
ON public.books FOR SELECT
USING (owner_id = auth.uid());

-- Books: owner can insert
CREATE POLICY "Books: owner can insert"
ON public.books FOR INSERT
WITH CHECK (owner_id = auth.uid());

-- Books: owner can update
CREATE POLICY "Books: owner can update"
ON public.books FOR UPDATE
USING (owner_id = auth.uid());

-- Repeat similar policies for chapters table
```

## Next Steps

1. ✅ Add `SUPABASE_JWT_SECRET` to your `.env` file
2. ✅ Install PyJWT: `pip install PyJWT`
3. ✅ Update your frontend to send JWT tokens
4. ✅ Enable RLS on Supabase tables
5. ✅ Create RLS policies
6. ✅ Test the authentication flow

## Optional: Protect Additional Endpoints

To protect other endpoints, simply add the dependency:

```python
@app.get("/books", response_model=List[Book])
async def list_books(current_user_id: str = Depends(get_current_user_id)):
    # Only return books owned by the current user
    books_dict = store.get_all_books()
    user_books = {k: v for k, v in books_dict.items() if v.get('owner_id') == current_user_id}
    return list(user_books.values())
```

## Troubleshooting

### "Token has expired"
- Tokens expire after a certain time (typically 1 hour)
- Frontend should refresh the token using `supabase.auth.refreshSession()`

### "Invalid token: Signature verification failed"
- Check that `SUPABASE_JWT_SECRET` matches your Supabase project's JWT secret
- Ensure the token is from the correct Supabase project

### "Not authenticated"
- Ensure Authorization header is present and formatted correctly: `Bearer <token>`
- Check that the token is not empty or null

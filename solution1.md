# Streamlit Saint API Debugging Analysis

## Current Behavior

Your Streamlit app sometimes displays the saint information correctly and sometimes returns an empty value. Based on the code, the most likely causes are hidden exceptions, API availability issues, session state caching, or timezone differences.

---

## How the Current Code Works

When the user opens the Streamlit application:

```python
if not st.session_state.today_loaded:
    st.session_state.liturgical_data = get_liturgical_day()
    st.session_state.readings = get_todays_readings()
    st.session_state.saint = get_saint_of_day()
    st.session_state.today_loaded = True
```

The saint data is loaded only once per browser session.

The `get_saint_of_day()` function:

1. Gets today's date.
2. Builds a URL to a JSON file hosted on GitHub Pages.
3. Calls the URL using `requests.get()`.
4. Parses the JSON response.
5. Extracts the celebration name.
6. Filters out ordinary liturgical days such as weekdays and Sundays.
7. Returns the saint name or an empty string.

---

## Main Problem: Exceptions Are Hidden

Current code:

```python
except:
    return ""
```

This catches every error and silently returns an empty string.

As a result, all of the following situations appear identical:

- Network timeout
- HTTP 404 error
- Invalid JSON
- API unavailable
- Data format change
- Genuine absence of a saint

The UI simply receives:

```python
""
```

and displays no saint.

---

## Recommended Change

Replace:

```python
except:
    return ""
```

with:

```python
except Exception as e:
    print(f"Saint API error: {e}")
    return ""
```

Or in Streamlit:

```python
except Exception as e:
    st.error(f"Saint API error: {e}")
    return ""
```

This allows you to see the actual failure.

---

## Possible Cause #1: Request Timeout

Current code:

```python
response = requests.get(url, timeout=5)
```

If GitHub Pages is temporarily slow, a timeout exception can occur.

Because all exceptions are swallowed, the function simply returns an empty string.

---

## Possible Cause #2: Missing JSON File

Example URL:

```text
https://cpbjr.github.io/catholic-readings-api/liturgical-calendar/2026/06-16.json
```

If the file does not exist, GitHub Pages returns:

```http
404 Not Found
```

The subsequent JSON parsing may fail.

Since the exception is hidden, the app returns an empty string.

---

## Possible Cause #3: API Structure Changes

The code assumes:

```json
{
  "celebration": {
    "name": "Saint John Francis Regis"
  }
}
```

If the API changes structure, for example:

```json
{
  "celebrations": [...]
}
```

then:

```python
celebration = data.get("celebration", {})
```

returns an empty dictionary and no saint name is found.

---

## Possible Cause #4: Session State Caching

Suppose:

1. User opens app.
2. API temporarily fails.
3. `get_saint_of_day()` returns `""`.
4. Streamlit stores:

```python
st.session_state.saint = ""
st.session_state.today_loaded = True
```

Even after the API becomes available again, the app does not retry because:

```python
today_loaded == True
```

The empty result remains cached for the rest of the session.

---

## Possible Cause #5: Timezone Differences

The code uses:

```python
today = date.today()
```

This uses the timezone of the server, not necessarily the user's timezone.

Example:

- User in Sydney: 17 June
- Server in United States: 16 June

The application may request the wrong JSON file around midnight, causing inconsistent results.

---

## Recommended Debug Version

```python
def get_saint_of_day():
    try:
        today = date.today()
        month_day = today.strftime("%m-%d")
        year = today.strftime("%Y")

        url = f"https://cpbjr.github.io/catholic-readings-api/liturgical-calendar/{year}/{month_day}.json"

        print(f"Fetching: {url}")

        response = requests.get(url, timeout=5)

        print(f"Status: {response.status_code}")

        response.raise_for_status()

        data = response.json()

        print(data)

        celebration = data.get("celebration", {})
        name = celebration.get("name", "")

        return name

    except Exception as e:
        print(f"Saint API error: {e}")
        return ""
```

---

## Most Likely Root Cause

The two most probable explanations are:

1. The GitHub-hosted JSON occasionally fails, times out, or returns an unexpected response.
2. A failed result is being cached in `st.session_state`, preventing future retries during the session.

Adding logging and `response.raise_for_status()` should quickly reveal which issue is occurring.

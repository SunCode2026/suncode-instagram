"""Send each given posts/<slug>/post.json to Buffer as an Instagram draft.
post.json: {"text": "...", "dueAt": "2026-10-27T11:30:00Z", "images": ["01.png", ...]}
env: BUFFER_API_KEY (secret), IMAGE_BASE (raw URL prefix ending in /), optional BUFFER_CHANNEL_ID."""
import json, os, sys, urllib.request

API = "https://api.buffer.com"
KEY = os.environ["BUFFER_API_KEY"]
MUTATION = ("mutation CreatePost($input: CreatePostInput!) { createPost(input: $input) { "
            "... on PostActionSuccess { post { id status dueAt } } ... on MutationError { message } } }")


def gql(query, variables=None):
    req = urllib.request.Request(API, json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 {"Content-Type": "application/json", "Authorization": f"Bearer {KEY}",
                                  "User-Agent": "suncode-instagram/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if out.get("errors"):
        raise SystemExit(f"Buffer API error: {out['errors']}")
    return out["data"]


def instagram_channel():
    if os.environ.get("BUFFER_CHANNEL_ID"):
        return os.environ["BUFFER_CHANNEL_ID"]
    orgs = gql("{ account { organizations { id } } }")["account"]["organizations"]
    for org in orgs:
        q = "query($o: String!) { channels(input: {organizationId: $o}) { id name service } }"
        for ch in gql(q, {"o": org["id"]})["channels"]:
            if ch["service"] == "instagram":
                return ch["id"]
    raise SystemExit("No Instagram channel connected in Buffer")


def build_input(post, folder, channel):
    base = os.environ["IMAGE_BASE"] + folder.strip("/") + "/"
    return {"channelId": channel, "text": post["text"], "schedulingType": "automatic",
            "mode": "customScheduled", "dueAt": post["dueAt"], "saveToDraft": True,
            "assets": {"images": [{"url": base + name} for name in post["images"]]}}


def main(paths):
    channel = instagram_channel()
    failed = 0
    for path in paths:
        post = json.load(open(path, encoding="utf-8"))
        res = gql(MUTATION, {"input": build_input(post, os.path.dirname(path), channel)})["createPost"]
        if "message" in res:
            failed += 1
            print(f"FAIL {path}: {res['message']}")
        else:
            print(f"OK   {path}: draft {res['post']['id']} for {res['post']['dueAt']}")
    if failed:
        # show the real input shape so a schema change is a one-line fix
        print(json.dumps(gql('{ __type(name: "CreatePostInput") { inputFields { name type { name kind ofType { name } } } } }'), indent=1))
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        os.environ["IMAGE_BASE"] = "https://raw.githubusercontent.com/o/r/sha/"
        i = build_input({"text": "t", "dueAt": "2026-10-27T11:30:00Z", "images": ["01.png", "02.png"]}, "posts/x", "c1")
        assert i["assets"]["images"][1]["url"] == "https://raw.githubusercontent.com/o/r/sha/posts/x/02.png"
        assert i["saveToDraft"] and i["mode"] == "customScheduled"
        print("selftest ok")
    else:
        main(sys.argv[1:])

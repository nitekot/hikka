from .schemas import CommentNode
from datetime import timedelta


# Convert uuid reference to comment path
def uuid_to_path(obj_uuid):
    return str(obj_uuid).replace("-", "_")


# Convert comment path to uuid reference
def path_to_uuid(obj_uuid):
    return str(obj_uuid).replace("_", "-")


def build_comments(base_comment, sub_comments):
    tree = CommentNode.create(path_to_uuid(base_comment.path), base_comment)
    tree_dict = {tree.reference: tree}

    for sub_comment in sub_comments:
        path = [path_to_uuid(element) for element in sub_comment.path]
        tree_node = tree_dict[path[0]]

        for path_node in path[1:]:
            reply = next(
                (
                    reply_node
                    for reply_node in tree_node.replies
                    if reply_node.reference == path_node
                ),
                None,
            )

            if not reply:
                reply = CommentNode.create(path_node)
                tree_node.replies.append(reply)
                tree_node.total_replies += 1
                tree_dict[path_node] = reply

            tree_node = reply

        tree_node.from_comment(sub_comment)

    return tree


# I really hate this
def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def round_hour(date):
    return date - timedelta(
        hours=date.hour % 1,
        minutes=date.minute,
        seconds=date.second,
        microseconds=date.microsecond,
    )
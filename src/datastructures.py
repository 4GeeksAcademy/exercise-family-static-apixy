"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = [
            {
                "id": self._generate_id(),
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jane",
                "last_name": last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jimmy",
                "last_name": last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]


    # This method generates a unique incremental ID
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member: dict):
        """
        Adds a member to the family.
        - If no 'id' is provided, generate one.
        - Default last_name to the family last_name.
        - Default lucky_numbers to empty list.
        Returns the normalized member dict.
        """
        new_member = {
            "id": member.get("id", self._generate_id()),
            "first_name": member["first_name"],
            "last_name": member.get("last_name", self.last_name),
            "age": member["age"],
            "lucky_numbers": member.get("lucky_numbers", []),
        }
        self._members.append(new_member)
        return new_member

    def delete_member(self, id: int) -> bool:
        """Deletes a member by id. Returns True if deleted, False if not found."""
        for idx, m in enumerate(self._members):
            if m["id"] == id:
                self._members.pop(idx)
                return True
        return False

    def get_member(self, id: int):
        """Returns the member with the given id or None if not found."""
        return next((m for m in self._members if m["id"] == id), None)

    # This method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

using Backend.Models;

namespace Backend.Services
{
    public class UserService
    {
        private readonly List<User> _users = new List<User>();

        // CREATE - הוספת משתמש חדש
        public void AddUser(User user)
        {
            user.Id = _users.Count > 0 ? _users.Max(u => u.Id) + 1 : 1;
            _users.Add(user);
        }

        // READ - שליפת משתמש לפי ID
        public User? GetUserById(int id)
        {
            return _users.FirstOrDefault(u => u.Id == id);
        }

        // READ - שליפת כל המשתמשים
        public List<User> GetAllUsers()
        {
            return _users;
        }

        // UPDATE - עדכון נתוני משתמש
        public bool UpdateUser(int id, User updatedUser)
        {
            var user = _users.FirstOrDefault(u => u.Id == id);
            if (user == null) return false;

            user.Name = updatedUser.Name;
            user.Email = updatedUser.Email;
            return true;
        }

        // DELETE - מחיקת משתמש לפי ID
        public bool DeleteUser(int id)
        {
            var user = _users.FirstOrDefault(u => u.Id == id);
            if (user == null) return false;

            _users.Remove(user);
            return true;
        }
    }
}

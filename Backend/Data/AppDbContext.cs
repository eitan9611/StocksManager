using Microsoft.EntityFrameworkCore;
using Backend.Models;

namespace Backend.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Stock> Stocks { get; set; }
        public DbSet<User> Users { get; set; }
        public DbSet<UserStock> UserStocks { get; set; }
        public DbSet<Trade> Trades { get; set; }


        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Composite key: UserEmail + Symbol
            modelBuilder.Entity<UserStock>()
                .HasKey(us => new { us.UserEmail, us.Symbol });

            // Relationship: UserStock → User (many-to-one)
            modelBuilder.Entity<UserStock>()
                .HasOne<User>()
                .WithMany(u => u.Portfolio)
                .HasForeignKey(us => us.UserEmail);
        }
    }

}

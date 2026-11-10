#include <iostream>
#include <string>
using namespace std;

class StarSystem;

class TravelRoute {
public:
    float travel_cost;
    StarSystem* destination;
    TravelRoute(float cost, StarSystem* dest) {
        travel_cost = cost;
        destination = dest;
    }
};

class StarSystem {
public:
    int system_id;
    string name;
    int num_planets;
    float x, y, z;
    bool is_habitable;
    TravelRoute** routes;   // array of edges to child systems, size M
    int num_routes;

    StarSystem(int id, string n, int planets, float px, float py, float pz, bool hab) {
        system_id = id;
        name = n;
        num_planets = planets;
        x = px;
        y = py;
        z = pz;
        is_habitable = hab;
        routes = nullptr;
        num_routes = 0;
    }
};

class Galaxy {
    int M;
    StarSystem* root;

    void print(StarSystem* s, int depth, float cost) const {
        cout << string(depth * 4, ' ') << s->name << " (id " << s->system_id
             << ", planets " << s->num_planets << ", (" << s->x << "," << s->y << "," << s->z << ")"
             << (s->is_habitable ? ", habitable" : "") << ")";
        if (depth > 0)
            cout << "  cost " << cost;
        cout << "\n";
        for (int i = 0; i < s->num_routes; i++)
            print(s->routes[i]->destination, depth + 1, s->routes[i]->travel_cost);
    }

public:
    Galaxy(int m) {
        M = m;
        root = nullptr;
    }
    Galaxy(int m, StarSystem* r) {
        M = m;
        root = r;
    }

    StarSystem* getRoot() const { return root; }

    bool addRoute(StarSystem* parent, StarSystem* child, float cost) {
        if (parent->num_routes >= M) {
            cout << "Cannot add " << child->name << ": " << parent->name
                 << " already has " << M << " routes\n";
            return false;
        }
        if (parent->routes == nullptr)
            parent->routes = new TravelRoute*[M];
        parent->routes[parent->num_routes++] = new TravelRoute(cost, child);
        return true;
    }

    int size(StarSystem* x) const {
        if (x == nullptr)
            return 0;
        int s = 1;
        for (int i = 0; i < x->num_routes; i++)
            s += size(x->routes[i]->destination);
        return s;
    }

    // balanced if at every node the child subtree sizes differ by at most 1;
    // missing children (fewer than M) count as size 0
    bool is_balanced(StarSystem* x) const {
        if (x == nullptr)
            return true;
        if (x->num_routes == 0)
            return true;
        int lo = size(x->routes[0]->destination);
        int hi = lo;
        for (int i = 0; i < x->num_routes; i++) {
            StarSystem* child = x->routes[i]->destination;
            int s = size(child);
            if (s < lo)
                lo = s;
            if (s > hi)
                hi = s;
            if (!is_balanced(child))
                return false;
        }
        if (x->num_routes < M)
            lo = 0;
        return hi - lo <= 1;
    }

    int count_leaves(StarSystem* x) const {
        if (x == nullptr)
            return 0;
        if (x->num_routes == 0)
            return 1;
        int c = 0;
        for (int i = 0; i < x->num_routes; i++)
            c += count_leaves(x->routes[i]->destination);
        return c;
    }

    void display() const {
        cout << "Galaxy (M = " << M << ", " << size(root) << " systems):\n";
        print(root, 0, 0);
    }
};

void report(const Galaxy& g) {
    g.display();
    cout << "Leaf systems: " << g.count_leaves(g.getRoot()) << "\n";
    cout << "Balanced    : " << (g.is_balanced(g.getRoot()) ? "yes" : "no") << "\n\n";
}

int main() {
    StarSystem* sol = new StarSystem(1, "Sol", 8, 0, 0, 0, true);
    StarSystem* alpha = new StarSystem(2, "Alpha Centauri", 3, 4.3, 0, 0, true);
    StarSystem* sirius = new StarSystem(3, "Sirius", 0, 8.6, 1, 2, false);
    StarSystem* vega = new StarSystem(4, "Vega", 2, 25, 3, -1, false);
    StarSystem* proxima = new StarSystem(5, "Proxima b", 1, 4.2, 0.1, 0, true);
    StarSystem* barnard = new StarSystem(6, "Barnard", 1, 6, -2, 1, false);
    StarSystem* rigel = new StarSystem(7, "Rigel", 4, 860, 10, 5, false);

    Galaxy g(3, sol);
    g.addRoute(sol, alpha, 4.5);
    g.addRoute(sol, sirius, 8.7);
    g.addRoute(sol, vega, 25.1);
    g.addRoute(alpha, proxima, 0.3);
    g.addRoute(sirius, barnard, 3.2);
    g.addRoute(vega, rigel, 830.0);
    g.addRoute(sol, rigel, 860.0);   // Sol is full (M = 3), rejected
    cout << "\n";
    report(g);

    // add two more systems under Alpha Centauri so its subtree gets bigger
    g.addRoute(alpha, new StarSystem(8, "Tau Ceti", 5, 12, 4, -3, true), 7.9);
    g.addRoute(alpha, new StarSystem(9, "Kepler-22", 1, 600, 20, 8, true), 590.0);
    cout << "\n";
    report(g);

    Galaxy empty(2);
    cout << "Empty galaxy leaves: " << empty.count_leaves(empty.getRoot())
         << ", balanced: " << (empty.is_balanced(empty.getRoot()) ? "yes" : "no") << "\n";
    return 0;
}

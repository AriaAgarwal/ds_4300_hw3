from fda_api import FDA_API

def create_visualizations(fda):
    fatal = fda.get_fatal_drugs(50, True)
    print(fatal)




def main() :
    fda = FDA_API()
    create_visualizations(fda)


if __name__ == "__main__":
    main()